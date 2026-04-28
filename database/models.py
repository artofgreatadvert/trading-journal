"""
Database models for the trading journal
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Trade(Base):
    """Trade model for storing trade information"""
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(50), nullable=False, index=True)
    trade_type = Column(String(50), nullable=False, index=True)
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    entry_date = Column(DateTime, nullable=False, index=True)
    exit_date = Column(DateTime, nullable=False, index=True)
    direction = Column(String(10), nullable=False)  # LONG or SHORT
    status = Column(String(20), default='Closed')  # OPEN, CLOSED, CANCELLED
    profit_loss = Column(Float, nullable=False)
    profit_loss_percent = Column(Float, nullable=False)
    commission = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    strategy = Column(String(100), nullable=True)
    risk_reward_ratio = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Trade(id={self.id}, symbol={self.symbol}, type={self.trade_type}, profit_loss={self.profit_loss})>"

    def to_dict(self):
        """Convert trade to dictionary"""
        return {
            'id': self.id,
            'symbol': self.symbol,
            'trade_type': self.trade_type,
            'entry_price': self.entry_price,
            'exit_price': self.exit_price,
            'quantity': self.quantity,
            'entry_date': self.entry_date.strftime('%Y-%m-%d %H:%M'),
            'exit_date': self.exit_date.strftime('%Y-%m-%d %H:%M'),
            'direction': self.direction,
            'status': self.status,
            'profit_loss': round(self.profit_loss, 2),
            'profit_loss_percent': round(self.profit_loss_percent, 2),
            'commission': round(self.commission, 2),
            'notes': self.notes or '',
            'strategy': self.strategy or '',
            'risk_reward_ratio': round(self.risk_reward_ratio, 2) if self.risk_reward_ratio else None
        }
