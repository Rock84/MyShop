from typing import Self

from sqlalchemy import select

from pydantic import Field, EmailStr, model_validator, field_validator
from ulid import new

from .base import DTO
from .custom_types import PasswordStr, MobileStr, AlphaStr
from src.datebase import User


class UserBasic(DTO):
    email: EmailStr = Field(
        default=...,
        title="User Email",
        description="Unique email",
        examples=["name_email@post_server.com", "nick@gmail.com"],
    )

    password: PasswordStr = Field(
        default=..., title="User Password", examples=["Password1!"]
    )


class UserLogin(UserBasic):
    @field_validator("email", mode="after")
    def email_validator(cls, email: str) -> str:
        with User.session as session:
            user = session.scalar(select(User).filter_by(email=email))
            if user is None:
                raise ValueError("user not found")
            return email

    @model_validator(mode="after")
    def password_validator(self) -> Self:
        with User.session as session:
            user = session.scalar(select(User).filter_by(email=self.email))
            if user is not None:
                return self
            raise ValueError("user not found")


class UserRegisterForm(UserBasic):
    name: AlphaStr = Field(default=..., min_length=2, max_length=64, title="User name")
    confirm_password: PasswordStr = Field(
        default=..., title="User confirm password", examples=["Qwerty1!"]
    )

    @field_validator("email", mode="after")
    def email_validator(cls, email: str) -> str:
        with User.session as session:
            user = session.scalar(select(User).filter_by(email=email))
            if user is not None:
                raise ValueError("email is not unqiue")
            return email

    @model_validator(mode="after")
    def validator_password(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Wrong password")
        if self.name.lower() in self.password.lower():
            raise ValueError("The password must not contain the username")
        if self.email.split("@")[0] in self.password.lower():
            raise ValueError("The password must not contain the Email name")
        if "password" in self.password.lower():
            raise ("The password must not contain the word 'password'")
        return self


class UserDetail(UserBasic):
    id: str = Field(
        default_factory=lambda: new().str,
        max_length=26,
        min_length=26,
        title="User identify",
        description="Universally Unique Lexicographically Sortable Identifier",
    )

    name: AlphaStr = Field(
        default=...,
        min_length=2,
        max_length=64,
        title="User name",
        examples=["Alex", "Вася"],
    )

    mobile: MobileStr = Field(
        default=...,
        title="User mobile number",
        examples=["+375291234567", "+79111234567"],
    )


class UserRechangePassword(UserRegisterForm):
    new_password: PasswordStr = Field(
        default=..., title="User new password", examples=["Qwerty1!"]
    )

    confirm_new_password: PasswordStr = Field(
        default=..., title="User confirm new password", examples=["Qwerty1!"]
    )

    def validator_password(self) -> Self:
        if self.new_password == self.confirm_new_password:
            raise ValueError("Entered your old password")
        if self.new_password != self.confirm_new_password:
            raise ValueError("Wrong password")
        if self.name.lower() in self.new_password.lower():
            raise ValueError("The password must not contain the username")
        if self.email.split("@")[0] in self.new_password.lower():
            raise ValueError("The password must not contain the Email name")
        if "password" in self.new_password.lower():
            raise ("The password must not contain the word 'password'")
        return self


class UserForgottenPassword(UserRegisterForm):
    temp_password: str = Field(
        default=..., title="User temp password", examples=["Qwerty1!"]
    )
