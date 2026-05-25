from peewee import SqliteDatabase, Model, CharField, FloatField, DateTimeField, ForeignKeyField, IntegerField
import datetime
import os

# Use a local SQLite database file
DB_PATH = os.environ.get('DB_PATH', 'misi_hedge_fund.db')
db = SqliteDatabase(DB_PATH)

class BaseModel(Model):
    class Meta:
        database = db

class PortfolioState(BaseModel):
    """Stores the overall portfolio balance and total value."""
    timestamp = DateTimeField(default=datetime.datetime.now)
    cash = FloatField()
    total_value = FloatField()

class Position(BaseModel):
    """Stores currently open positions."""
    ticker = CharField(unique=True)
    units = FloatField()
    entry_price = FloatField()
    last_price = FloatField()
    timestamp = DateTimeField(default=datetime.datetime.now)

class Trade(BaseModel):
    """Stores a history of all executed trades."""
    ticker = CharField()
    side = CharField() # 'BUY' or 'SELL'
    units = FloatField()
    price = FloatField()
    reason = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now)

def init_db():
    db.connect(reuse_if_open=True)
    db.create_tables([PortfolioState, Position, Trade])
