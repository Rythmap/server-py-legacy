import toml
from fastapi_mail import ConnectionConfig
from passlib.context import CryptContext
from pymongo import MongoClient

# Read and parse the TOML configuration file
data = toml.load("config.toml")

# Access values from the parsed TOML data
server_address = data.get("server_address")
update_accounts_interval = data.get("update_accounts_interval", 10)
websocket_interval = data.get("websocket_interval", 1)
path_prefix_end = data.get("path_prefix_end", "/")
max_distance = data.get("max_distance", 5)
max_upload_size = data.get("max_upload_size", 157286400)
user_data_directory = data.get("user_data_directory")

spotify_client_id = data.get("spotify_client_id", "")
spotify_client_secret = data.get("spotify_client_secret", "")
spotify_redirect_uri = data.get("spotify_redirect_uri", "")

mongo_private_url = data.get("mongo_private_url", "")

# Check if email part is enabled
email_enabled = data.get("email_enabled", True)
print(email_enabled)
if email_enabled:
    # Access fastapi_mail settings
    fastapi_mail_settings = data.get("fastapi_mail", {})
    conf = ConnectionConfig(
        MAIL_NICKNAME=fastapi_mail_settings.get("MAIL_NICKNAME", ""),
        MAIL_PASSWORD=fastapi_mail_settings.get("MAIL_PASSWORD", ""),
        MAIL_FROM=fastapi_mail_settings.get("MAIL_FROM", ""),
        MAIL_PORT=fastapi_mail_settings.get("MAIL_PORT", 587),
        MAIL_SERVER=fastapi_mail_settings.get("MAIL_SERVER", ""),
        MAIL_FROM_NAME=fastapi_mail_settings.get("MAIL_FROM_NAME", ""),
        MAIL_STARTTLS=fastapi_mail_settings.get("MAIL_STARTTLS", True),
        MAIL_SSL_TLS=fastapi_mail_settings.get("MAIL_SSL_TLS", False),
        USE_CREDENTIALS=fastapi_mail_settings.get("USE_CREDENTIALS", True),
        VALIDATE_CERTS=fastapi_mail_settings.get("VALIDATE_CERTS", True),
    )

client = MongoClient(mongo_private_url)

db = client["melomap"]

account_collection = db["accounts"]
recovery_token_collection = db["recovery_tokens"]
confirm_token_collection = db["confirm_tokens"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
