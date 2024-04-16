# Codes
INVALID_NICKNAME_OR_PASSWORD = 400
"""Invalid nickname or password

The user submitted invalid credentials.
"""

INVALID_NICKNAME = 401
"""Invalid nickname

The nickname must contain only English characters and numbers.
"""

INVALID_NICKNAME_LENGTH = 402
"""Invalid nickname length

The length of the nickname must be between 3 and 32 characters.
"""

INVALID_PASSWORD_LENGTH = 403
"""Invalid password length

The length of the password must be between 6 and 64 characters.
"""

NO_USER = 404
"""No user

There is no user with this nickname.
"""

INVALID_TOKEN = 405
"""Invalid token

The token is invalid or expired.
"""

NICKNAME_ALREADY_REGISTERED = 406
"""Nickname already registered

The nickname is already registered.
"""

NICKNAME_CHANGE_FAILED = 407
"""Nickname change failed

The nickname change failed.
"""

INVALID_RECOVERY_TOKEN = 408
"""Invalid recovery token

The recovery token is invalid or expired.
"""

EXPIRED_OR_INVALID_TOKEN = 409
"""Expired or invalid token

The token is expired or invalid.
"""

EMAIL_ALREADY_EXISTS = 410
"""Email already exists

The email is already registered.
"""

INVALID_NICKNAME_OR_EMAIL = 411
"""Invalid nickname or email

The nickname or email is invalid.
"""
# Descriptions
INVALID_NICKNAME_OR_PASSWORD_DETAIL = "Invalid nickname or password" 
"""Invalid nickname or password

The user submitted invalid credentials.
"""

INVALID_NICKNAME_DETAIL = "Nickname must contain only English characters and numbers" 
"""Invalid nickname

The nickname must contain only English characters and numbers.
"""

INVALID_NICKNAME_LENGTH_DETAIL = "Nickname length must be between 3 and 32 characters" 
"""Invalid nickname length

The length of the nickname must be between 3 and 32 characters.
"""

INVALID_PASSWORD_LENGTH_DETAIL = "Password length must be between 6 and 64 characters" 
"""Invalid password length

The length of the password must be between 6 and 64 characters.
"""

INVALID_TOKEN_DETAIL = "Invalid token" 
"""Invalid token

The token is invalid or expired.
"""

NO_USER_DETAIL = "There is no user with this nickname" 
"""No user

There is no user with this nickname.
"""

NICKNAME_ALREADY_REGISTERED_DETAIL = "Nickname already registered" 
"""Nickname already registered

The nickname is already registered.
"""

NICKNAME_CHANGE_FAILED_DETAIL = "Nickname change failed" 
"""Nickname change failed

The nickname change failed.
"""

# Errors related to password recovery
INVALID_RECOVERY_TOKEN_DETAIL = "Recover token is invalid" 
"""Invalid recovery token

The recovery token is invalid or expired.
"""

EXPIRED_OR_INVALID_TOKEN_DETAIL = "Token is expired or invalid" 
"""Expired or invalid token

The token is expired or invalid.
"""

# Errors related to account creation
EMAIL_ALREADY_EXISTS_DETAIL = "Email already exists" 
"""Email already exists

The email is already registered.
"""

INVALID_NICKNAME_OR_EMAIL_DETAIL = "Invalid nickname or email" 
"""Invalid nickname or email

The nickname or email is invalid.
"""

