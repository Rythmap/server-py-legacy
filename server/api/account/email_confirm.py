import random
import string
from datetime import datetime, timedelta

from fastapi import APIRouter, BackgroundTasks, Query
from fastapi_mail import FastMail, MessageSchema

from utils.config_parser import *
from utils.errors import *
from models.account_models import *
from utils.validators import *

router = APIRouter()


@router.post(f"{path_prefix_end}account.confirm_email")
async def confirm_email(confirm_email: ConfirmEmail, background_tasks: BackgroundTasks):
    user = get_user_by_token(confirm_email.token)
    check_email_confirmed(user)
    confirm_token = "".join(random.choice(string.digits) for _ in range(6))
    expiration_time = datetime.utcnow() + timedelta(hours=1)
    confirm_token_collection.insert_one(
        {
            "nickname": user["nickname"],
            "email": user["email"],
            "confirm_token": confirm_token,
            "expiration_time": expiration_time,
        }
    )
    confirmation_link = f"{server_address}/melomap/api/account.confirm_email_link?confirm_token={confirm_token}"
    message = MessageSchema(
        subject="Email Confirmation",
        recipients=[user["email"]],
        body=f"""Your code: {confirm_token}
        Click <a href="{confirmation_link}">here</a> to confirm your email.""",
        subtype="html",
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

    return {"status": "email confirmation initiated"}


@router.get(f"{path_prefix_end}account.confirm_email_link")
async def confirm_email_link(confirm_token: str = Query(...)):
    confirm_user = get_user_by_confirm_token(confirm_token)
    if (
        confirm_user["confirm_token"] == None
        or confirm_user["expiration_time"] < datetime.utcnow()
    ):
        raise HTTPException(
            status_code=EXPIRED_OR_INVALID_TOKEN, detail=EXPIRED_OR_INVALID_TOKEN_DETAIL
        )

    nickname = confirm_user["nickname"]

    account_collection.update_one(
        {"nickname": nickname}, {"$set": {"email_confirmed": True}}
    )

    confirm_token_collection.delete_one(
        {"confirm_token": confirm_user["confirm_token"]}
    )

    return {"status": "email successfully confirmed"}
