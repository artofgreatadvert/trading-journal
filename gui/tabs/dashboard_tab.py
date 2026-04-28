"""
Dashboard tab - Shows trading summary and statistics
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout,
    QPushButton, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from database.db_manager import DatabaseManager
from datetime import datetime, timedelta


class DashboardTab(QWidget):
    """Dashboard tab widget"""

    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()
        self.refresh_data()

    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # Title
        title = QLabel("Trading Dashboard")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)

        # Statistics Grid
        stats_layout = QGridLayout()
        stats_layout.setSpacing(10)

        self.total_trades_label = self.create_stat_card("Total Trades", "0", QColor(66, 133, 244))
        self.win_rate_label = self.create_stat_card("Win Rate", "0%", QColor(52, 168, 83))
        self.total_profit_label = self.create_stat_card("Total Profit", "$0.00", QColor(251, 188, 4))
        self.avg_profit_label = self.create_stat_card("Avg. Profit", "$0.00", QColor(156, 39, 176))

        stats_layout.addWidget(self.total_trades_label, 0, 0)
        stats_layout.addWidget(self.win_rate_label, 0, 1)
        stats_layout.addWidget(self.total_profit_label, 0, 2)
        stats_layout.addWidget(self.avg_profit_label, 0, 3)

        main_layout.addLayout(stats_layout)

        # Chart for recent trades
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(self.chart_view.renderHints())
        main_layout.addWidget(self.chart_view)

        # Buttons
        button_layout = QHBoxLayout()
        refresh_btn = QPushButton("Refresh Data")
        refresh_btn.clicked.connect(self.refresh_data)
        button_layout.addStretch()
        button_layout.addWidget(refresh_btn)

        main_layout.addLayout(button_layout)
        main_layout.addStretch()

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

        # Store reference to value label for updating
        card.value_label = value_label
        return card

    def refresh_data(self):
        """Refresh dashboard data"""
        try:
            stats = self.db_manager.get_statistics('all')

            # Update stat cards
            self.total_trades_label.value_label.setText(str(stats['total_trades']))
            self.win_rate_label.value_label.setText(f"{stats['win_rate']}%")
            self.total_profit_label.value_label.setText(f"${stats['total_profit']:.2f}")
            self.avg_profit_label.value_label.setText(f"${stats['average_profit']:.2f}")

            # Update chart with recent trades
            self.update_chart()

        except Exception as e:
            print(f"Error refreshing dashboard: {e}")

    def update_chart(self):
        """Update the chart with recent trades data"""
        try:
            trades = self.db_manager.get_all_trades()[-7:]  # Last 7 trades

            if not trades:
                return

            chart = QChart()
            chart.setTitle("Recent 7 Trades Performance")

            bar_set = QBarSet("Profit/Loss")
            categories = []

            for i, trade in enumerate(trades):
                bar_set.append(trade.profit_loss)
                categories.append(f"Trade {i + 1}")

                # Color code: green for profit, red for loss
                if trade.profit_loss > 0:
                    bar_set.setColor(QColor(52, 168, 83))  # Green
                else:
                    bar_set.setColor(QColor(229, 57, 53))  # Red

            series = QBarSeries()
            series.append(bar_set)
            chart.addSeries(series)

            axisX = QBarCategoryAxis()
            axisX.append(categories)
            chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
            series.attachAxis(axisX)

            axisY = QValueAxis()
            chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
            series.attachAxis(axisY)

            self.chart_view.setChart(chart)

        except Exception as e:
            print(f"Error updating chart: {e}")
