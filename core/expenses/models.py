from sqlalchemy import Float, Integer, Column, String, ForeignKey, DateTime, func
from core.database import Base
from sqlalchemy.orm import relationship


class ExpenseModel(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    desc = Column(String(50))
    amount = Column(Float)
    expense_date = Column(DateTime, server_default=func.now())

    user = relationship("UserModel", back_populates="expenses")
