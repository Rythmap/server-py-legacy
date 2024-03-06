import asyncio
from fastapi import APIRouter, WebSocket
from configs.mongo import *
from configs.app_config import *
import json
from utils.validators import *


router = APIRouter()


class AccountUpdater:
    def __init__(self, interval=10):
        self.accounts = None
        self.interval = interval

    async def update_accounts(self):
        while True:
            if self.accounts is not None:
                new_accounts = list(
                    map(
                        lambda x: {
                            str(x["_id"]): {
                                "nickname": x["username"],
                                "geolocation": self.accounts.get(str(x["_id"]), {}).get(
                                    "geolocation", None
                                ),
                            }
                        },
                        (account_collection.find({}, {"_id": 1, "username": 1})),
                    )
                )
                new_accounts = {k: v for d in new_accounts for k, v in d.items()}
                self.accounts.update(new_accounts)
            else:
                self.accounts = list(
                    map(
                        lambda x: {
                            str(x["_id"]): {
                                "nickname": x["username"],
                                "geolocation": None,
                            }
                        },
                        (account_collection.find({}, {"_id": 1, "username": 1})),
                    )
                )
                self.accounts = {k: v for d in self.accounts for k, v in d.items()}
            print(self.accounts, type(self.accounts))
            await asyncio.sleep(self.interval)


account_updater = AccountUpdater(interval=update_accounts_interval)


@router.on_event("startup")
async def startup_event():
    asyncio.create_task(account_updater.update_accounts())


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(str(data))
        data = json.loads(data)
        access_token = data.get("access_token")
        geolocation = data.get("geolocation")

        if access_token:
            user_doc = get_user_by_token(access_token)
            if user_doc:
                user_id = str(user_doc["_id"])
                if account_updater.accounts[user_id]["geolocation"] is None:
                    account_updater.accounts[user_id]["geolocation"] = geolocation

        if account_updater.accounts:
            await websocket.send_text(str(account_updater.accounts))
        await asyncio.sleep(websocket_interval)
