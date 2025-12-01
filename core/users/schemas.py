from datetime import datetime
from pydantic import Field, BaseModel, field_validator


class UserBaseSchema(BaseModel):
    username: str = Field(
        ..., min_length=5, max_length=250, description="Username of the user"
    )
    password: str = Field(
        ..., min_length=6, description="Password of the user"
    )


class UserLoginSchema(UserBaseSchema):
    pass


class UserRegisterSchema(UserBaseSchema):
    password_confirm: str = Field(
        ..., description="Confirm password of the user"
    )

    @field_validator("password_confirm")
    def check_password_match(cls, password_confirm, validation):
        if not (password_confirm == validation.data.get("password")):
            raise ValueError("password doesnt match.")
        return password_confirm


class UserResponseSchema(BaseModel):
    username: str


class UserRefreshTokenSchema(BaseModel):
    token: str = Field(..., description="refresh token of the user")
