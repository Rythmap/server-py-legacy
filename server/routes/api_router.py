from fastapi import APIRouter
from melomap.api import router as api
from melomap.emailconfirm import router as emailconfirm
from melomap.pswdrecovery import router as pswdrecovery
from melomap.ws import router as wsrouter

router = APIRouter(tags=["Melomap"])

api_prefix = "/melomap"

router.include_router(api, prefix=api_prefix)
router.include_router(emailconfirm, prefix=api_prefix)
router.include_router(pswdrecovery, prefix=api_prefix)
router.include_router(wsrouter, prefix=api_prefix)

