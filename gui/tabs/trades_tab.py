"""
Trades tab - Manage and view trades
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QDateEdit, QDialog, QFormLayout, QSpinBox, QDoubleSpinBox,
    QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QDate, QDateTime
from PyQt6.QtGui import QColor, QFont
from database.db_manager import DatabaseManager
from config.settings import TRADE_TYPES
from datetime import datetime


class TradesTab(QWidget):
    """Trades tab widget"""

    def __init__(self, db_manager: DatabaseManager, on_trade_updated=None):
        super().__init__()
        self.db_manager = db_manager
        self.on_trade_updated = on_trade_updated
        self.init_ui()
        self.refresh_trades()

    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        # Title
        title = QLabel("Trades Management")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)

        # Search and filter layout
        filter_layout = QHBoxLayout()

        filter_layout.addWidget(QLabel("Symbol:"))
        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("Enter symbol (e.g., AAPL)")
        filter_layout.addWidget(self.symbol_input)

        filter_layout.addWidget(QLabel("Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItem("All")
        self.type_combo.addItems(TRADE_TYPES)
        filter_layout.addWidget(self.type_combo)

        filter_layout.addWidget(QLabel("From:"))
        self.from_date = QDateEdit()
        self.from_date.setDate(QDate.currentDate().addMonths(-1))
        filter_layout.addWidget(self.from_date)

        filter_layout.addWidget(QLabel("To:"))
        self.to_date = QDateEdit()
        self.to_date.setDate(QDate.currentDate())
        filter_layout.addWidget(self.to_date)

        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_trades)
        filter_layout.addWidget(search_btn)

        main_layout.addLayout(filter_layout)

        # Table
        self.trades_table = QTableWidget()
        self.trades_table.setColumnCount(11)
        self.trades_table.setHorizontalHeaderLabels([
            "ID", "Symbol", "Type", "Direction", "Entry", "Exit",
            "Quantity", "Entry Date", "Exit Date", "P&L", "P&L %"
        ])
        self.trades_table.horizontalHeader().setStretchLastSection(False)
        self.trades_table.setSelectionBehavior(self.trades_table.SelectionBehavior.SelectRows)
        self.trades_table.setSelectionMode(self.trades_table.SelectionMode.SingleSelection)
        main_layout.addWidget(self.trades_table)

        # Buttons layout
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Add Trade")
        add_btn.clicked.connect(self.add_trade)
        button_layout.addWidget(add_btn)

        edit_btn = QPushButton("Edit Trade")
        edit_btn.clicked.connect(self.edit_trade)
        button_layout.addWidget(edit_btn)

        delete_btn = QPushButton("Delete Trade")
        delete_btn.clicked.connect(self.delete_trade)
        delete_btn.setStyleSheet("background-color: #f44336; color: white;")
        button_layout.addWidget(delete_btn)

        button_layout.addStretch()
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_trades)
        button_layout.addWidget(refresh_btn)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def refresh_trades(self):
        """Refresh the trades table"""
        try:
            trades = self.db_manager.get_all_trades()
            self.populate_table(trades)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to refresh trades: {e}")

    def search_trades(self):
        """Search trades based on filters"""
        try:
            symbol = self.symbol_input.text() or None
            trade_type = self.type_combo.currentText()
            if trade_type == "All":
                trade_type = None
            start_date = datetime.combine(self.from_date.date().toPyDate(), datetime.min.time())
            end_date = datetime.combine(self.to_date.date().toPyDate(), datetime.max.time())

            trades = self.db_manager.search_trades(
                symbol=symbol,
                trade_type=trade_type,
                start_date=start_date,
                end_date=end_date
            )
            self.populate_table(trades)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Search failed: {e}")

    def populate_table(self, trades):
        """Populate the trades table"""
        self.trades_table.setRowCount(len(trades))

        for row, trade in enumerate(trades):
            self.trades_table.setItem(row, 0, QTableWidgetItem(str(trade.id)))
            self.trades_table.setItem(row, 1, QTableWidgetItem(trade.symbol))
            self.trades_table.setItem(row, 2, QTableWidgetItem(trade.trade_type))
            self.trades_table.setItem(row, 3, QTableWidgetItem(trade.direction))
            self.trades_table.setItem(row, 4, QTableWidgetItem(f"${trade.entry_price:.2f}"))
            self.trades_table.setItem(row, 5, QTableWidgetItem(f"${trade.exit_price:.2f}"))
            self.trades_table.setItem(row, 6, QTableWidgetItem(f"{trade.quantity:.2f}"))
            self.trades_table.setItem(row, 7, QTableWidgetItem(trade.entry_date.strftime("%Y-%m-%d %H:%M")))
            self.trades_table.setItem(row, 8, QTableWidgetItem(trade.exit_date.strftime("%Y-%m-%d %H:%M")))

            # Profit/Loss with color coding
            pl_item = QTableWidgetItem(f"${trade.profit_loss:.2f}")
            if trade.profit_loss > 0:
                pl_item.setForeground(QColor(52, 168, 83))  # Green
            elif trade.profit_loss < 0:
                pl_item.setForeground(QColor(229, 57, 53))  # Red
            self.trades_table.setItem(row, 9, pl_item)

            # Profit/Loss Percentage
            pl_pct_item = QTableWidgetItem(f"{trade.profit_loss_percent:.2f}%")
            if trade.profit_loss_percent > 0:
                pl_pct_item.setForeground(QColor(52, 168, 83))
            elif trade.profit_loss_percent < 0:
                pl_pct_item.setForeground(QColor(229, 57, 53))
            self.trades_table.setItem(row, 10, pl_pct_item)

    def add_trade(self):
        """Open dialog to add a new trade"""
        dialog = TradeDialog(self, edit_mode=False)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            trade_data = dialog.get_trade_data()
            try:
                self.db_manager.add_trade(trade_data)
                self.refresh_trades()
                if self.on_trade_updated:
                    self.on_trade_updated()
                QMessageBox.information(self, "Success", "Trade added successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add trade: {e}")

    def edit_trade(self):
        """Edit selected trade"""
        selected_row = self.trades_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a trade to edit.")
            return

        trade_id = int(self.trades_table.item(selected_row, 0).text())
        trades = self.db_manager.get_all_trades()
        trade = next((t for t in trades if t.id == trade_id), None)

        if trade:
            dialog = TradeDialog(self, edit_mode=True, trade=trade)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                trade_data = dialog.get_trade_data()
                try:
                    self.db_manager.update_trade(trade_id, trade_data)
                    self.refresh_trades()
                    if self.on_trade_updated:
                        self.on_trade_updated()
                    QMessageBox.information(self, "Success", "Trade updated successfully!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to update trade: {e}")

    def delete_trade(self):
        """Delete selected trade"""
        selected_row = self.trades_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a trade to delete.")
            return

        trade_id = int(self.trades_table.item(selected_row, 0).text())
        reply = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this trade?")

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db_manager.delete_trade(trade_id)
                self.refresh_trades()
                if self.on_trade_updated:
                    self.on_trade_updated()
                QMessageBox.information(self, "Success", "Trade deleted successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete trade: {e}")


class TradeDialog(QDialog):
    """Dialog for adding/editing trades"""

    def __init__(self, parent=None, edit_mode=False, trade=None):
        super().__init__(parent)
        self.edit_mode = edit_mode
        self.trade = trade
        self.init_ui()
        if edit_mode and trade:
            self.populate_fields(trade)

    def init_ui(self):
        """Initialize dialog UI"""
        self.setWindowTitle("Add Trade" if not self.edit_mode else "Edit Trade")
        self.setGeometry(100, 100, 500, 600)

        layout = QFormLayout()

        # Symbol
        self.symbol_input = QLineEdit()
        layout.addRow("Symbol:", self.symbol_input)

        # Type
        self.type_combo = QComboBox()
        self.type_combo.addItems(TRADE_TYPES)
        layout.addRow("Trade Type:", self.type_combo)

        # Direction
        self.direction_combo = QComboBox()
        self.direction_combo.addItems(["LONG", "SHORT"])
        layout.addRow("Direction:", self.direction_combo)

        # Entry Price
        self.entry_price = QDoubleSpinBox()
        self.entry_price.setDecimals(2)
        self.entry_price.setMaximum(9999999)
        layout.addRow("Entry Price:", self.entry_price)

        # Exit Price
        self.exit_price = QDoubleSpinBox()
        self.exit_price.setDecimals(2)
        self.exit_price.setMaximum(9999999)
        layout.addRow("Exit Price:", self.exit_price)

        # Quantity
        self.quantity = QDoubleSpinBox()
        self.quantity.setDecimals(4)
        self.quantity.setMaximum(9999999)
        self.quantity.setValue(1)
        layout.addRow("Quantity:", self.quantity)

        # Entry Date
        self.entry_date = QDateEdit()
        self.entry_date.setDate(QDate.currentDate())
        layout.addRow("Entry Date:", self.entry_date)

        # Exit Date
        self.exit_date = QDateEdit()
        self.exit_date.setDate(QDate.currentDate())
        layout.addRow("Exit Date:", self.exit_date)

        # Commission
        self.commission = QDoubleSpinBox()
        self.commission.setDecimals(2)
        self.commission.setMaximum(9999999)
        layout.addRow("Commission:", self.commission)

        # Strategy
        self.strategy = QLineEdit()
        layout.addRow("Strategy:", self.strategy)

        # Notes
        self.notes = QTextEdit()
        self.notes.setMaximumHeight(100)
        layout.addRow("Notes:", self.notes)

        # Buttons
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addRow(button_layout)

        self.setLayout(layout)

    def populate_fields(self, trade):
        """Populate fields with trade data"""
        self.symbol_input.setText(trade.symbol)
        self.type_combo.setCurrentText(trade.trade_type)
        self.direction_combo.setCurrentText(trade.direction)
        self.entry_price.setValue(trade.entry_price)
        self.exit_price.setValue(trade.exit_price)
        self.quantity.setValue(trade.quantity)
        self.entry_date.setDate(trade.entry_date.date())
        self.exit_date.setDate(trade.exit_date.date())
        self.commission.setValue(trade.commission)
        self.strategy.setText(trade.strategy or "")
        self.notes.setPlainText(trade.notes or "")

    def get_trade_data(self) -> dict:
        """Get trade data from form"""
        return {
            'symbol': self.symbol_input.text().upper(),
            'trade_type': self.type_combo.currentText(),
            'direction': self.direction_combo.currentText(),
            'entry_price': self.entry_price.value(),
            'exit_price': self.exit_price.value(),
            'quantity': self.quantity.value(),
            'entry_date': datetime.combine(self.entry_date.date().toPyDate(), datetime.min.time()),
            'exit_date': datetime.combine(self.exit_date.date().toPyDate(), datetime.max.time()),
            'commission': self.commission.value(),
            'strategy': self.strategy.text(),
            'notes': self.notes.toPlainText(),
        }
