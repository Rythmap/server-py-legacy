from typing import Literal, Union
from pydantic import BaseModel, EmailStr


class Register(BaseModel):
    nickname: str
    password: str
    email: Union[EmailStr, Literal[""]]


class Login(BaseModel):
    nickname: str
    password: str


class ResetToken(BaseModel):
    nickname: str
    password: str


class DeleteAccount(BaseModel):
    nickname: str
    password: str


class ChangePassword(BaseModel):
    nickname: str
    current_password: str
    new_password: str


class ChangeNickname(BaseModel):
    token: str
    new_nickname: str


class RecoverPassword(BaseModel):
    nickname: str


class ConfirmEmail(BaseModel):
    token: str


class ConfirmRecovery(BaseModel):
    recovery_token: str
    new_password: str

