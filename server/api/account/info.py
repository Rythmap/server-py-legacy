from fastapi import APIRouter

from models.account_models import *
from utils.random_digits import *
from utils.validators import *
from utils.config_parser import *
from utils.errors import *

router = APIRouter()

@router.get(
    f"{path_prefix_end}account.info",
    summary="Get account info",
    responses={
        200: {"content": {"application/json": {}}},
        401: {"description": INVALID_TOKEN_DETAIL},
        404: {"description": NO_USER_DETAIL},
    },
)
async def get_account_info(token: str):
    """Get account info"""
    user = get_user_by_token(token)
    return {
        "nickname": user["nickname"],
        "email": user["email"],
        "email_confirmed": user["email_confirmed"],
    }
