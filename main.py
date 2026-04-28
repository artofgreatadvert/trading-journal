#!/usr/bin/env python3
"""
Trading Journal Desktop Application
Main entry point for the application
"""

import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
from database.db_manager import DatabaseManager


def main():
    # Initialize database
    db_manager = DatabaseManager()
    db_manager.init_db()
    
    # Create and run the application
    app = QApplication(sys.argv)
    window = MainWindow(db_manager)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
