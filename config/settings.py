"""
Application settings and configuration
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

# Database
DATABASE_URL = f'sqlite:///{DATA_DIR}/trading_journal.db'

# Trade types
TRADE_TYPES = [
    'Stocks',
    'Forex',
    'Crypto',
    'Options',
    'Futures',
    'Commodities',
    'Other'
]

# Application settings
APP_TITLE = 'Trading Journal'
APP_VERSION = '1.0.0'
APP_AUTHOR = 'Trading Journal Developer'

# UI Settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
DEFAULT_CURRENCY = 'USD'

# Analysis periods
ANALYSIS_PERIODS = {
    'Today': 'today',
    'This Week': 'week',
    'This Month': 'month',
    'This Year': 'year',
    'All Time': 'all'
}
