from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    email = Column(String)
    password = Column(String(15))
    expenses = relationship("Expense", backref="user", uselist=True, cascade="all, delete-orphan")

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    desc = Column(String(50))
    amount = Column(Float)
    expense_date = Column(DateTime, default=datetime.datetime.now())


def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
