import uuid


def create_access_token() -> str:
    """
    Creates a new access token

    Returns:
        The new access token
    """
    return str(uuid.uuid4())