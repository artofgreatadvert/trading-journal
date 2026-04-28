"""
Analysis tab - Detailed trading analysis and statistics
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGridLayout, QFrame, QComboBox, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtChart import QChart, QChartView, QLineSeries
from PyQt6.QtCore import QPointF
from database.db_manager import DatabaseManager
from datetime import datetime, timedelta


class AnalysisTab(QWidget):
    """Analysis tab widget"""

    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()
        self.refresh_data()

    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        # Title
        title = QLabel("Trading Analysis")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)

        # Period selector
        period_layout = QHBoxLayout()
        period_layout.addWidget(QLabel("Analysis Period:"))
        self.period_combo = QComboBox()
        self.period_combo.addItems(["Today", "This Week", "This Month", "This Year", "All Time"])
        self.period_combo.currentTextChanged.connect(self.on_period_changed)
        period_layout.addWidget(self.period_combo)
        period_layout.addStretch()
        main_layout.addLayout(period_layout)

        # Statistics Grid
        stats_layout = QGridLayout()
        stats_layout.setSpacing(10)

        self.total_trades_label = self.create_stat_card("Total Trades", "0", QColor(66, 133, 244))
        self.winning_trades_label = self.create_stat_card("Winning Trades", "0", QColor(52, 168, 83))
        self.losing_trades_label = self.create_stat_card("Losing Trades", "0", QColor(229, 57, 53))
        self.win_rate_label = self.create_stat_card("Win Rate", "0%", QColor(156, 39, 176))
        self.total_profit_label = self.create_stat_card("Total Profit", "$0.00", QColor(251, 188, 4))
        self.avg_profit_label = self.create_stat_card("Avg. Profit", "$0.00", QColor(33, 150, 243))
        self.best_trade_label = self.create_stat_card("Best Trade", "$0.00", QColor(76, 175, 80))
        self.worst_trade_label = self.create_stat_card("Worst Trade", "$0.00", QColor(244, 67, 54))

        stats_layout.addWidget(self.total_trades_label, 0, 0)
        stats_layout.addWidget(self.winning_trades_label, 0, 1)
        stats_layout.addWidget(self.losing_trades_label, 0, 2)
        stats_layout.addWidget(self.win_rate_label, 0, 3)
        stats_layout.addWidget(self.total_profit_label, 1, 0)
        stats_layout.addWidget(self.avg_profit_label, 1, 1)
        stats_layout.addWidget(self.best_trade_label, 1, 2)
        stats_layout.addWidget(self.worst_trade_label, 1, 3)

        main_layout.addLayout(stats_layout)

        # Chart
        self.chart_view = QChartView()
        main_layout.addWidget(self.chart_view)

        # Details table
        self.details_table = QTableWidget()
        self.details_table.setColumnCount(5)
        self.details_table.setHorizontalHeaderLabels(["Symbol", "Type", "Entry", "Exit", "P&L"])
        main_layout.addWidget(self.details_table)

        # Refresh button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_data)
        button_layout.addWidget(refresh_btn)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def create_stat_card(self, title: str, value: str, color: QColor) -> QFrame:
        """Create a statistic card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                border-radius: 8px;
                background-color: white;
                border-left: 4px solid rgb({color.red()}, {color.green()}, {color.blue()});
                padding: 15px;
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)

        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(9)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #666666;")

        value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(14)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setStyleSheet(f"color: rgb({color.red()}, {color.green()}, {color.blue()});")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()

        card.value_label = value_label
        return card

    def on_period_changed(self):
        """Handle period change"""
        self.refresh_data()

    def refresh_data(self):
        """Refresh analysis data"""
        try:
            period_map = {
                "Today": "today",
                "This Week": "week",
                "This Month": "month",
                "This Year": "year",
                "All Time": "all"
            }
            period = period_map[self.period_combo.currentText()]
            stats = self.db_manager.get_statistics(period)

            # Update stat cards
            self.total_trades_label.value_label.setText(str(stats['total_trades']))
            self.winning_trades_label.value_label.setText(str(stats['winning_trades']))
            self.losing_trades_label.value_label.setText(str(stats['losing_trades']))
            self.win_rate_label.value_label.setText(f"{stats['win_rate']}%")
            self.total_profit_label.value_label.setText(f"${stats['total_profit']:.2f}")
            self.avg_profit_label.value_label.setText(f"${stats['average_profit']:.2f}")
            self.best_trade_label.value_label.setText(f"${stats['best_trade']:.2f}")
            self.worst_trade_label.value_label.setText(f"${stats['worst_trade']:.2f}")

            # Update chart
            self.update_cumulative_chart(period)

            # Update details table
            self.update_details_table(period)

        except Exception as e:
            print(f"Error refreshing analysis: {e}")

    def update_cumulative_chart(self, period: str):
        """Update cumulative profit chart"""
        try:
            # Get trades for the period
            if period == 'today':
                start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                trades = [t for t in self.db_manager.get_all_trades() if t.exit_date >= start_date]
            elif period == 'week':
                start_date = datetime.now() - timedelta(days=7)
                trades = [t for t in self.db_manager.get_all_trades() if t.exit_date >= start_date]
            elif period == 'month':
                start_date = datetime.now() - timedelta(days=30)
                trades = [t for t in self.db_manager.get_all_trades() if t.exit_date >= start_date]
            elif period == 'year':
                start_date = datetime.now() - timedelta(days=365)
                trades = [t for t in self.db_manager.get_all_trades() if t.exit_date >= start_date]
            else:
                trades = self.db_manager.get_all_trades()

            if not trades:
                return

            # Sort by date
            trades.sort(key=lambda t: t.exit_date)

            # Create chart
            chart = QChart()
            chart.setTitle("Cumulative Profit/Loss")

            series = QLineSeries()
            cumulative = 0
            for i, trade in enumerate(trades):
                cumulative += trade.profit_loss
                series.append(QPointF(i, cumulative))

            chart.addSeries(series)
            chart.createDefaultAxes()
            self.chart_view.setChart(chart)

        except Exception as e:
            print(f"Error updating chart: {e}")

    def update_details_table(self, period: str):
        """Update details table"""
        try:
            # Get trades for the period
            if period == 'today':
                start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                trades = [t for t in self.db_manager.get_all_trades() if t.exit_date >= start_date]
            elif period == 'week':
                start_date = datetime.now() - timedelta(days=7)
                trades = [t for t in self.db_manager.get_all_trades() if t.exit_date >= start_date]
            elif period == 'month':
                start_date = datetime.now() - timedelta(days=30)
                trades = [t for t in self.db_manager.get_all_trades() if t.exit_date >= start_date]
            elif period == 'year':
                start_date = datetime.now() - timedelta(days=365)
                trades = [t for t in self.db_manager.get_all_trades() if t.exit_date >= start_date]
            else:
                trades = self.db_manager.get_all_trades()

            self.details_table.setRowCount(len(trades))
            for row, trade in enumerate(trades):
                self.details_table.setItem(row, 0, QTableWidgetItem(trade.symbol))
                self.details_table.setItem(row, 1, QTableWidgetItem(trade.trade_type))
                self.details_table.setItem(row, 2, QTableWidgetItem(f"${trade.entry_price:.2f}"))
                self.details_table.setItem(row, 3, QTableWidgetItem(f"${trade.exit_price:.2f}"))
                
                pl_item = QTableWidgetItem(f"${trade.profit_loss:.2f}")
                if trade.profit_loss > 0:
                    pl_item.setForeground(QColor(52, 168, 83))
                elif trade.profit_loss < 0:
                    pl_item.setForeground(QColor(229, 57, 53))
                self.details_table.setItem(row, 4, pl_item)

        except Exception as e:
            print(f"Error updating details table: {e}")
