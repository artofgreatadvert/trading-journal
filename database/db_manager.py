"""
Database manager for handling all database operations
"""

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
from config.settings import DATABASE_URL
from database.models import Base, Trade
from typing import List, Optional, Dict, Tuple


class DatabaseManager:
    """Manages all database operations"""

    def __init__(self):
        self.engine = create_engine(DATABASE_URL, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def init_db(self):
        """Initialize database tables"""
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()

    def add_trade(self, trade_data: Dict) -> Trade:
        """Add a new trade to the database"""
        session = self.get_session()
        try:
            # Calculate profit/loss
            if trade_data['direction'].upper() == 'LONG':
                profit_loss = (trade_data['exit_price'] - trade_data['entry_price']) * trade_data['quantity']
            else:  # SHORT
                profit_loss = (trade_data['entry_price'] - trade_data['exit_price']) * trade_data['quantity']

            profit_loss -= trade_data.get('commission', 0)

            # Calculate profit/loss percentage
            entry_cost = trade_data['entry_price'] * trade_data['quantity']
            profit_loss_percent = (profit_loss / entry_cost * 100) if entry_cost != 0 else 0

            trade = Trade(
                symbol=trade_data['symbol'].upper(),
                trade_type=trade_data['trade_type'],
                entry_price=trade_data['entry_price'],
                exit_price=trade_data['exit_price'],
                quantity=trade_data['quantity'],
                entry_date=trade_data['entry_date'],
                exit_date=trade_data['exit_date'],
                direction=trade_data['direction'].upper(),
                status=trade_data.get('status', 'Closed'),
                profit_loss=profit_loss,
                profit_loss_percent=profit_loss_percent,
                commission=trade_data.get('commission', 0),
                notes=trade_data.get('notes', ''),
                strategy=trade_data.get('strategy', ''),
                risk_reward_ratio=trade_data.get('risk_reward_ratio')
            )
            session.add(trade)
            session.commit()
            session.close()
            return trade
        except Exception as e:
            session.close()
            raise e

    def get_all_trades(self) -> List[Trade]:
        """Get all trades from database"""
        session = self.get_session()
        try:
            trades = session.query(Trade).order_by(Trade.exit_date.desc()).all()
            session.close()
            return trades
        except Exception as e:
            session.close()
            raise e

    def get_trades_by_type(self, trade_type: str) -> List[Trade]:
        """Get trades filtered by type"""
        session = self.get_session()
        try:
            trades = session.query(Trade).filter(Trade.trade_type == trade_type).all()
            session.close()
            return trades
        except Exception as e:
            session.close()
            raise e

    def get_trades_by_symbol(self, symbol: str) -> List[Trade]:
        """Get trades filtered by symbol"""
        session = self.get_session()
        try:
            trades = session.query(Trade).filter(Trade.symbol == symbol.upper()).all()
            session.close()
            return trades
        except Exception as e:
            session.close()
            raise e

    def get_trades_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Trade]:
        """Get trades within a date range"""
        session = self.get_session()
        try:
            trades = session.query(Trade).filter(
                Trade.exit_date >= start_date,
                Trade.exit_date <= end_date
            ).order_by(Trade.exit_date.desc()).all()
            session.close()
            return trades
        except Exception as e:
            session.close()
            raise e

    def search_trades(self, symbol: Optional[str] = None, trade_type: Optional[str] = None,
                     start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Trade]:
        """Search trades with multiple filters"""
        session = self.get_session()
        try:
            query = session.query(Trade)

            if symbol:
                query = query.filter(Trade.symbol.ilike(f'%{symbol}%'))
            if trade_type:
                query = query.filter(Trade.trade_type == trade_type)
            if start_date:
                query = query.filter(Trade.exit_date >= start_date)
            if end_date:
                query = query.filter(Trade.exit_date <= end_date)

            trades = query.order_by(Trade.exit_date.desc()).all()
            session.close()
            return trades
        except Exception as e:
            session.close()
            raise e

    def update_trade(self, trade_id: int, trade_data: Dict) -> Optional[Trade]:
        """Update an existing trade"""
        session = self.get_session()
        try:
            trade = session.query(Trade).filter(Trade.id == trade_id).first()
            if trade:
                for key, value in trade_data.items():
                    if hasattr(trade, key):
                        setattr(trade, key, value)
                trade.updated_at = datetime.utcnow()
                session.commit()
            session.close()
            return trade
        except Exception as e:
            session.close()
            raise e

    def delete_trade(self, trade_id: int) -> bool:
        """Delete a trade"""
        session = self.get_session()
        try:
            trade = session.query(Trade).filter(Trade.id == trade_id).first()
            if trade:
                session.delete(trade)
                session.commit()
                session.close()
                return True
            session.close()
            return False
        except Exception as e:
            session.close()
            raise e

    def get_statistics(self, period: str = 'all') -> Dict:
        """Get trading statistics for a given period"""
        session = self.get_session()
        try:
            query = session.query(Trade)

            # Apply period filter
            if period == 'today':
                start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                query = query.filter(Trade.exit_date >= start_date)
            elif period == 'week':
                start_date = datetime.now() - timedelta(days=7)
                query = query.filter(Trade.exit_date >= start_date)
            elif period == 'month':
                start_date = datetime.now() - timedelta(days=30)
                query = query.filter(Trade.exit_date >= start_date)
            elif period == 'year':
                start_date = datetime.now() - timedelta(days=365)
                query = query.filter(Trade.exit_date >= start_date)

            trades = query.all()
            session.close()

            if not trades:
                return self._empty_statistics()

            total_trades = len(trades)
            winning_trades = len([t for t in trades if t.profit_loss > 0])
            losing_trades = len([t for t in trades if t.profit_loss < 0])
            total_profit = sum([t.profit_loss for t in trades])
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            average_profit = total_profit / total_trades if total_trades > 0 else 0

            return {
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'losing_trades': losing_trades,
                'total_profit': round(total_profit, 2),
                'win_rate': round(win_rate, 2),
                'average_profit': round(average_profit, 2),
                'best_trade': round(max([t.profit_loss for t in trades]), 2) if trades else 0,
                'worst_trade': round(min([t.profit_loss for t in trades]), 2) if trades else 0,
            }
        except Exception as e:
            session.close()
            raise e

    @staticmethod
    def _empty_statistics() -> Dict:
        """Return empty statistics"""
        return {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_profit': 0,
            'win_rate': 0,
            'average_profit': 0,
            'best_trade': 0,
            'worst_trade': 0,
        }
