"""
Main application window
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont
from config.settings import APP_TITLE, APP_VERSION, WINDOW_WIDTH, WINDOW_HEIGHT
from gui.tabs.dashboard_tab import DashboardTab
from gui.tabs.trades_tab import TradesTab
from gui.tabs.analysis_tab import AnalysisTab
from database.db_manager import DatabaseManager


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(f"{APP_TITLE} v{APP_VERSION}")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        # Create header
        header_layout = QHBoxLayout()
        title_label = QLabel(f"{APP_TITLE} v{APP_VERSION}")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        # Create tab widget
        self.tabs = QTabWidget()

        # Create tabs
        self.dashboard_tab = DashboardTab(self.db_manager)
        self.trades_tab = TradesTab(self.db_manager, self.on_trade_updated)
        self.analysis_tab = AnalysisTab(self.db_manager)

        # Add tabs
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(self.trades_tab, "Trades")
        self.tabs.addTab(self.analysis_tab, "Analysis")

        main_layout.addWidget(self.tabs)

        # Set styles
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 5px 15px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
            }
        """)

    def on_trade_updated(self):
        """Callback when a trade is updated"""
        # Refresh dashboard and analysis tabs
        self.dashboard_tab.refresh_data()
        self.analysis_tab.refresh_data()
        QMessageBox.information(self, "Success", "Trade data updated successfully!")
