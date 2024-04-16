import os
from utils.config_parser import *

async def remove_file(filename: str):
    try:
        file_path = os.path.join(user_data_directory, filename)
        os.remove(file_path)
        return {"message": f"File {filename} removed successfully"}
    except FileNotFoundError:
        return {"message": f"File {filename} not found"}
