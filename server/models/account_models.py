from pydantic import BaseModel, EmailStr
from typing import Union, Literal

class Account(BaseModel):
    username: str
    password: str
    email: Union[EmailStr, Literal[""]]


class AccountLogin(BaseModel):
    username: str
    password: str


class ChangePassword(BaseModel):
    username: str
    current_password: str
    new_password: str


class ChangeNickname(BaseModel):
    token: str
    new_username: str


class RecoverPassword(BaseModel):
    username: str


class Token(BaseModel):
    token: str


class ConfirmEmail(BaseModel):
    token: str


class ConfirmRecovery(BaseModel):
    recovery_token: str
    new_password: str