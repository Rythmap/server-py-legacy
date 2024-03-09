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
                new_accounts = {
                    k: v for d in new_accounts for k, v in d.items()}
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
                self.accounts = {
                    k: v for d in self.accounts for k, v in d.items()}
            print(self.accounts, type(self.accounts))
            await asyncio.sleep(self.interval)


account_updater = AccountUpdater(interval=update_accounts_interval)


@router.on_event("startup")
async def startup_event():
    asyncio.create_task(account_updater.update_accounts())


def validate_geolocation(geolocation):
    if geolocation is None:
        return None
    if not isinstance(geolocation, dict):
        return None
    if 'latitude' not in geolocation or 'longitude' not in geolocation:
        return None
    try:
        lat = float(geolocation['latitude'])
        lon = float(geolocation['longitude'])
        if lat < -90 or lat > 90 or lon < -180 or lon > 180:
            return None
    except ValueError:
        return None
    return geolocation

from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(str(data))
        data = json.loads(data)
        access_token = data.get("access_token")
        geolocation = validate_geolocation(data.get("geolocation"))

        if access_token:
            user_doc = get_user_by_token(access_token)
            if user_doc:
                user_id = str(user_doc["_id"])
                if account_updater.accounts[user_id]["geolocation"] is None:
                    account_updater.accounts[user_id]["geolocation"] = geolocation

        if account_updater.accounts and geolocation:
            filtered_accounts = {}
            for id, account in account_updater.accounts.items():
                account_geolocation = account.get("geolocation")
                if account_geolocation:
                    distance = haversine(geolocation['longitude'], geolocation['latitude'], account_geolocation['longitude'], account_geolocation['latitude'])
                    if distance <= 5:  # 5 kilometers
                        filtered_accounts[id] = account
            await websocket.send_text(str(filtered_accounts))
        await asyncio.sleep(websocket_interval)
