from pydantic import BaseModel, Field, EmailStr
from datetime import date


NAME_MAX_LENGTH = 30
DESC_MAX_LENGTH = 50
PASSWORD_MIN_LENGTH = 4
PASSWORD_MAX_LENGTH = 15
AMOUNT_MIN_VALUE = 0


class BaseExpenseSchema(BaseModel):
    id: int
    user_id: int
    desc: str = Field(..., max_length=DESC_MAX_LENGTH)
    amount: float = Field(..., gt=AMOUNT_MIN_VALUE)
    expense_date: date


class CreateExpenseSchema(BaseModel):
    desc: str = Field(..., max_length=DESC_MAX_LENGTH)
    amount: float = Field(..., gt=AMOUNT_MIN_VALUE)
    expense_date: date | None = None

class BaseUserSchema(BaseModel):
    id: int
    name: str = Field(..., max_length=NAME_MAX_LENGTH)
    email: EmailStr | None = None
    expenses: list[BaseExpenseSchema] = []


class CreateUserSchema(BaseModel):
    name: str = Field(..., max_length=NAME_MAX_LENGTH)
    email: EmailStr | None = None
    password: str = Field(..., min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH)
