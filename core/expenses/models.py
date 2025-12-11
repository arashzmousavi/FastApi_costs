from sqlalchemy import (
    Float,
    Integer,
    Column,
    String,
    ForeignKey,
    DateTime,
    func,
)
from core.database import Base
from sqlalchemy.orm import relationship


class ExpenseModel(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    desc = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    expense_date = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship("UserModel", back_populates="expenses")
