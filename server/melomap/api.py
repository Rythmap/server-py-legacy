from utils.validators import *
from utils.random_digits import *
from fastapi import APIRouter
from models.account_models import *
import uuid


router = APIRouter()

def create_access_token():
    return str(uuid.uuid4())

@router.post("/account.register")
async def register(account: Account):
    validate_username(account.username)
    validate_username_length(account.username)
    validate_password_length(account.password)
    check_existing_username(account.username)
    check_existing_email(account.email)

    hashed_password = pwd_context.hash(account.password)
    access_token = create_access_token()
    account_collection.insert_one(
        {
            "account_id": get_random_digits_str(32),
            "username": account.username,
            "password": hashed_password,
            "email": account.email,
            "token": access_token,
            "email_confirmed": False
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/account.login")
async def login(account: AccountLogin):
    user = get_user_by_username_or_email(account.username)
    validate_user_credentials(user, account.password)
    return {"access_token": user["token"], "token_type": "bearer"}


@router.get("/account.info")
async def login(token: str):
    user = get_user_by_token(token)
    return {"token_valid": True, "username": user["username"], "email": user["email"],
            "email_confirmed": user["email_confirmed"]}

@router.post("/account.token.reset")
async def reset_token(account: AccountLogin):
    user = get_user_by_username(account.username)
    validate_user_credentials(user, account.password)

    new_token = create_access_token()
    account_collection.update_one(
        {"username": account.username}, {"$set": {"token": new_token}}
    )
    return {"access_token": new_token, "token_type": "bearer"}

@router.post("/account.changenick")
async def change_nickname(change_nickname: ChangeNickname):
    validate_username(change_nickname.new_username)
    validate_username_length(change_nickname.new_username)
    check_existing_username(change_nickname.new_username)

    result = account_collection.update_one(
        {"token": change_nickname.token}, {"$set": {"username": change_nickname.new_username}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=USERNAME_CHANGE_FAILED, detail=USERNAME_CHANGE_FAILED_DETAIL)

    return {"status": "username changed"}


@router.post("/account.changepswd")
async def change_password(change_password: ChangePassword):
    user = get_user_by_username(change_password.username)
    validate_user_credentials(user, change_password.current_password)
    validate_password_length(change_password.new_password)

    hashed_password = pwd_context.hash(change_password.new_password)
    account_collection.update_one(
        {"username": change_password.username}, {"$set": {"password": hashed_password}}
    )
    return {"status": "password changed"}


@router.delete("/account.delete")
async def delete_account(account: AccountLogin):
    user = get_user_by_username(account.username)
    validate_user_credentials(user, account.password)
    account_collection.delete_one(user)
    return {"status": "account deleted"}