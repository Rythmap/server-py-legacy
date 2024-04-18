from fastapi import APIRouter, File, UploadFile
from utils.config_parser import *
from utils.errors import *
from utils.validators import *
from utils.remove_file import remove_file
import logging
import random, string
from fastapi.responses import FileResponse

router = APIRouter()

logger = logging.getLogger(__name__) 

@router.post("/upload-avatar")
async def upload_avatar(token: str, file: UploadFile):
    logger.info("test")    
    user = get_user_by_token(token)
    avatar = user.get("avatar", None)
    if avatar is not None:
        await remove_file(avatar)
    if (
        file.content_type in ["image/jpeg", "image/png"]
        and file.size <= max_upload_size
    ):
        try:
            random_filename = "".join(
                random.choice(string.ascii_letters + string.digits) for _ in range(16)
            )
            with open(f"{user_data_directory}/{random_filename}", "wb") as f:
                while contents := file.file.read(1024 * 1024):
                    f.write(contents)
        except Exception as error:
            logging.error("An error occured while uploading the avatar: %s", error)
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()

        account_collection.update_one(
            {"_id": user["_id"]}, {"$set": {"avatar": random_filename}}
        )

        return {"message": f"Successfully uploaded"}


@router.get("/avatar/{nickname}")
async def main(nickname):
    user = get_user_by_nickname(nickname)
    avatar = user.get("avatar", None)
    if avatar is None:
        return {"message": f"No avatar"}
    else:
        try:
            return FileResponse(
                f"{user_data_directory}/{avatar}", media_type="image/png"
            )
        except RuntimeError as error:
            logging.error("An error occured while sending the avatar: %s", error)
            return {"message": f"Avatar"}
