from pydantic import BaseModel, field_validator, Field
from uuid import UUID

class BaseCheckSchema(BaseModel):
    id: UUID
    desc: str = Field(..., description="Enter your description, max 50 characters.")
    amount: float

    @field_validator("desc")
    def validate_desc(cls, value):
        if len(value) > 50:
            raise ValueError("Please enter less than 50 characters.")
        return value

    @field_validator("amount")
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("Amount must be greater than 0.")
        return value

class CreateCostSchema(BaseModel):
    desc: str = Field(..., description="Enter your description, max 50 characters.")
    amount: float

    @field_validator("desc")
    def validate_desc(cls, value):
        if len(value) > 50:
            raise ValueError("Please enter less than 50 characters.")
        return value

    @field_validator("amount")
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("Amount must be greater than 0.")
        return value