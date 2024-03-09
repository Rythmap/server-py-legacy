import os

"""Configuration of the Melodymap server app

Contains the server address, the update accounts interval, the websocket
interval, the path prefix end, and the maximum distance in meters to show
accounts for the user.

The values are read from the environment variables, if they are not set the
default values are used.
"""

server_address = os.environ.get("SERVER_ADDRESS", None)
"""The server address to listen on, None for default"""

update_accounts_interval = int(os.environ.get("UPDATE_ACCOUNTS_INTERVAL", 10))
"""The interval in seconds to update the accounts from the Spotify API"""

websocket_interval = int(os.environ.get("WEBSOCKET_INTERVAL", 1))
"""The interval in seconds to send the accounts to the client through websocket"""

path_prefix_end = os.environ.get("PATH_PREFIX_END", "/")
"""The path prefix end to use for the server"""

max_distance = int(os.environ.get("MAX_DISTANCE", 5))
"""The maximum distance in meters to show accounts for the user"""