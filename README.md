# Trading Journal Desktop Application

A comprehensive desktop application for logging, tracking, and analyzing your trading activity. Built with Python using PyQt6 for the GUI and SQLAlchemy for database management.

## Features

### 📊 Dashboard
- Real-time trading statistics
- Visual charts showing recent trade performance
- Quick overview of profit/loss and win rates
- Automatic data refresh

### 📝 Trade Management
- Add, edit, and delete trades
- Support for multiple trade types (Stocks, Forex, Crypto, Options, Futures, Commodities, Other)
- Search and filter trades by:
  - Symbol
  - Trade type
  - Date range
- Color-coded profit/loss visualization
- Detailed trade information display

### 📈 Analysis
- Period-based analysis (Today, Week, Month, Year, All Time)
- Cumulative profit/loss charting
- Detailed statistics:
  - Total trades
  - Winning/losing trades
  - Win rate
  - Average profit
  - Best and worst trades
- Trade details table with filtering

## Trade Types Supported

- Stocks/Equities
- Forex
- Cryptocurrencies
- Options
- Futures
- Commodities
- Other

## Quick Start

### Option 1: Run from Source

1. **Clone the repository**
```bash
git clone https://github.com/artofgreatadvert/trading-journal.git
cd trading-journal
```

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Run the application**
```bash
python main.py
```

### Option 2: Build as Executable

1. **Download and extract repository**

2. **Run build script**

**Windows:**
```bash
build.bat
```

**Mac/Linux:**
```bash
bash build.sh
```

3. **Find executable**
- Windows: `dist/Trading Journal.exe`
- Mac/Linux: `dist/Trading Journal`

## Requirements

- Python 3.8+
- PyQt6 (included in requirements)
- SQLAlchemy (included in requirements)
- Pandas (included in requirements)
- Matplotlib (included in requirements)

## Usage

### Adding a Trade
1. Click the **"Add Trade"** button in the Trades tab
2. Fill in the trade details:
   - Symbol (e.g., AAPL, EUR/USD)
   - Trade type
   - Direction (LONG or SHORT)
   - Entry and exit prices
   - Quantity
   - Dates
   - Optional: Commission, Strategy, Notes
3. Click **"OK"** to save

### Searching Trades
1. Use the search filters in the Trades tab:
   - Enter a symbol
   - Select trade type
   - Choose date range
2. Click **"Search"** to filter results

### Viewing Analytics
1. Switch to the **Analysis** tab
2. Select a time period from the dropdown
3. View statistics and cumulative profit/loss chart
4. See detailed trade information in the table below

## Project Structure

```
trading-journal/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── build_exe.py           # Executable build script
├── build.bat              # Windows build script
├── build.sh               # Mac/Linux build script
├── README.md              # This file
├── config/
│   ├── __init__.py
│   └── settings.py        # Application configuration
├── database/
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy models
│   └── db_manager.py      # Database operations
├── gui/
│   ├── __init__.py
│   ├── main_window.py     # Main window
│   └── tabs/
│       ├── __init__.py
│       ├── dashboard_tab.py  # Dashboard tab
│       ├── trades_tab.py     # Trades management tab
│       └── analysis_tab.py   # Analysis tab
└── tests/
    ├── __init__.py
    └── test_db_manager.py # Unit tests
```

## Database

The application uses SQLite for data storage. The database file is created automatically in the `data/` directory as `trading_journal.db`.

## Calculations

### Profit/Loss
- **LONG**: `(Exit Price - Entry Price) × Quantity - Commission`
- **SHORT**: `(Entry Price - Exit Price) × Quantity - Commission`

### Win Rate
`(Winning Trades / Total Trades) × 100`

### Average Profit
`Total Profit / Total Trades`

## Troubleshooting

### Database Issues
If you encounter database errors, delete the `data/trading_journal.db` file and restart the application.

### Display Issues
If charts don't display correctly:
1. Ensure you have at least one trade logged
2. Try clicking "Refresh" button

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Feel free to submit a Pull Request.

## Support

For issues or questions, please create an issue in the GitHub repository.
