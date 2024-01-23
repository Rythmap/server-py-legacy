from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi import BackgroundTasks
from utils.validators import *
from fastapi import APIRouter
from models.account_models import *
import random
import string
from datetime import datetime, timedelta
from configs.app_config import *
from configs.email import *

router = APIRouter()

@router.post("/melomap/api/account.recoverpswd")
async def recover_password(recover_password: RecoverPassword, background_tasks: BackgroundTasks):
    account = get_user_by_username(recover_password.username)
    recovery_token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
    expiration_time = datetime.utcnow() + timedelta(hours=1)
    recovery_token_collection.insert_one({
        "username": recover_password.username,
        "email": account["email"],
        "recovery_token": recovery_token,
        "expiration_time": expiration_time
    })
    print([account["email"]])
    message = MessageSchema(
        subject="Password Recovery",
        recipients=[account["email"]],
        body=f"Your code: {recovery_token}",
        subtype="html"
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

    return {"status": "password recovery initiated"}


@router.post("/melomap/api/account.confirm_recovery")
async def confirm_recovery(confirm_recovery: ConfirmRecovery):
    recovery_token = confirm_recovery.recovery_token
    new_password = confirm_recovery.new_password
    validate_password_length(new_password)
    recover_user = get_user_by_recovery_token(recovery_token)
    print(recover_user["recovery_token"])
    if recover_user["recovery_token"] == None or recover_user["expiration_time"] < datetime.utcnow():
        raise HTTPException(status_code=EXPIRED_OR_INVALID_TOKEN, detail=EXPIRED_OR_INVALID_TOKEN_DETAIL)

    username = recover_user["username"]

    hashed_password = pwd_context.hash(new_password)
    account_collection.update_one({"username": username}, {"$set": {"password": hashed_password}})

    recovery_token_collection.delete_one({"recovery_token": recover_user["recovery_token"]})

    return {"status": "password successfully changed"}
