from sqlalchemy import Integer, Column, String, ForeignKey, DateTime, func
from core.database import Base
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now())

    token = relationship("TokenModel", back_populates="user", uselist=False)
    expenses = relationship(
        "ExpenseModel", back_populates="user", cascade="all, delete-orphan")

    def hash_password(self, raw_password: str) -> str:
        return pwd_context.hash(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        return pwd_context.verify(raw_password, self.password)

    def set_password(self, raw_password: str) -> None:
        self.password = self.hash_password(raw_password)


class TokenModel(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    users_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, nullable=False, unique=True)
    created_token = Column(DateTime, server_default=func.now())

    user = relationship("UserModel", back_populates="token", uselist=False)
