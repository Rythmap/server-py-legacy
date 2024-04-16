from fastapi import APIRouter

from api.account.change_nickname import router as change_nickname
from api.account.change_password import router as change_password
from api.account.delete import router as delete
from api.account.info import router as info
from api.account.login import router as login
from api.account.register import router as register
from api.account.reset_token import router as reset_token
from api.account.email_confirm import router as email_confirm
from api.account.pswdrecovery import router as pswdrecovery
from api.account.upload_avatar import router as upload_avatar

router = APIRouter(tags=["Rythmap"])

api_prefix = "/rythmap"

router.include_router(register)
router.include_router(login)
router.include_router(info)
router.include_router(reset_token)
router.include_router(change_nickname)
router.include_router(change_password)
router.include_router(delete)
router.include_router(email_confirm)
router.include_router(pswdrecovery)
router.include_router(upload_avatar)