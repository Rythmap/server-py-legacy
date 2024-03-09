import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from configs.mongo import *
from configs.app_config import *
import json
from utils.validators import *
from typing import Optional


router = APIRouter()


class AccountUpdater:
    def __init__(self, interval=10):
        self.accounts = None
        self.interval = interval

    async def update_accounts(self):
        """Update the accounts dictionary with the current data from the database.

        The accounts dictionary has the user's _id as key and a dictionary with
        username and geolocation as value.
        """
        # Initialize the accounts dictionary with the data from the database
        new_accounts = {
            str(x["_id"]): {
                "username": x["username"],
                "geolocation": None
            }
            for x in account_collection.find({}, {"_id": 1, "username": 1})
        }

        # Update the accounts dictionary with the new data from the database
        while True:
            self.accounts = new_accounts

            # Add the new accounts to the accounts dictionary
            new_accounts = {
                str(x["_id"]): {
                    "username": x["username"],
                    "geolocation": self.accounts.get(str(x["_id"]), {}).get(
                        "geolocation", None
                    )
                }
                for x in account_collection.find({}, {"_id": 1, "username": 1})
            }

            # Update the accounts dictionary with the new data
            self.accounts.update(new_accounts)

            # Print the accounts dictionary and its type for debugging
            print(self.accounts, type(self.accounts))

            await asyncio.sleep(self.interval)


account_updater = AccountUpdater(interval=update_accounts_interval)


@router.on_event("startup")
async def startup_event() -> None:
    """Create an asynchronous task to update the accounts dictionary
    periodically when the server starts up.

    The accounts dictionary is updated using the update_accounts method of the
    AccountUpdater class.
    """
    asyncio.create_task(account_updater.update_accounts())


def validate_geolocation(geolocation: dict) -> Optional[dict]:
    """
    Validate the geolocation dictionary.

    The function returns None if the geolocation dictionary is invalid,
    otherwise it returns the validated geolocation dictionary.

    A geolocation dictionary is considered valid if all of the following
    conditions are met:

    1. It is not None
    2. It is a dictionary
    3. It contains the keys 'latitude' and 'longitude'
    4. The values of the keys 'latitude' and 'longitude' can be converted to
       floats without raising a ValueError
    5. The values of the keys 'latitude' and 'longitude' are between -90 and 90
       for latitude and between -180 and 180 for longitude
    """
    if geolocation is None:
        return None

    if not isinstance(geolocation, dict):
        return None

    if 'latitude' not in geolocation or 'longitude' not in geolocation:
        return None

    try:
        lat = float(geolocation['latitude'])
        lon = float(geolocation['longitude'])
    except ValueError:
        return None

    if lat < -90 or lat > 90 or lon < -180 or lon > 180:
        return None

    return geolocation

from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points on the earth
    (specified in decimal degrees)

    The haversine formula is used to calculate the distance between two
    points which are located on the surface of a sphere (in this case, the
    Earth). It is a more efficient and accurate method than calculating
    the distance using Euclidean geometry.

    Args:
        lon1 (float): Longitude of the first point in decimal degrees
        lat1 (float): Latitude of the first point in decimal degrees
        lon2 (float): Longitude of the second point in decimal degrees
        lat2 (float): Latitude of the second point in decimal degrees

    Returns:
        float: The distance between the two points in kilometers
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers.
    return c * r

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Websocket endpoint for Melodymap"""

    async def update_client():
        """Send the filtered accounts dictionary to the client"""
        if account_updater.accounts and geolocation:
            filtered_accounts = {}
            for id, account in account_updater.accounts.items():
                account_geolocation = account.get("geolocation")
                if account_geolocation:
                    distance = haversine(
                        geolocation["longitude"], geolocation["latitude"],
                        account_geolocation["longitude"], account_geolocation["latitude"]
                    )
                    if distance <= max_distance:
                        filtered_accounts[id] = account
            await websocket.send_text(str(filtered_accounts))

    async def main_loop():
        """Main loop of the websocket endpoint"""
        while True:
            await update_client()
            await asyncio.sleep(websocket_interval)

    print("Websocket connection established")
    await websocket.accept()

    while True:
        try:
            data = await websocket.receive_text()
        except WebSocketDisconnect:
            print("Websocket connection closed")
            break
        data = json.loads(data)
        access_token = data.get("access_token")
        geolocation = validate_geolocation(data.get("geolocation"))

        if access_token:
            user_doc = get_user_by_token(access_token)
            if user_doc:
                user_id = str(user_doc["_id"])
                if account_updater.accounts[user_id]["geolocation"] is None:
                    account_updater.accounts[user_id]["geolocation"] = geolocation

        await main_loop()
