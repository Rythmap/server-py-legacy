# Codes
INVALID_USERNAME_OR_PASSWORD = 400
"""Invalid username or password

The user submitted invalid credentials.
"""

INVALID_USERNAME = 401
"""Invalid username

The username must contain only English characters and numbers.
"""

INVALID_USERNAME_LENGTH = 402
"""Invalid username length

The length of the username must be between 3 and 32 characters.
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

USERNAME_ALREADY_REGISTERED = 406
"""Username already registered

The username is already registered.
"""

USERNAME_CHANGE_FAILED = 407
"""Username change failed

The username change failed.
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

INVALID_USERNAME_OR_EMAIL = 411
"""Invalid username or email

The username or email is invalid.
"""
# Descriptions
INVALID_USERNAME_OR_PASSWORD_DETAIL = "Invalid username or password" 
"""Invalid username or password

The user submitted invalid credentials.
"""

INVALID_USERNAME_DETAIL = "Username must contain only English characters and numbers" 
"""Invalid username

The username must contain only English characters and numbers.
"""

INVALID_USERNAME_LENGTH_DETAIL = "Username length must be between 3 and 32 characters" 
"""Invalid username length

The length of the username must be between 3 and 32 characters.
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

USERNAME_ALREADY_REGISTERED_DETAIL = "Username already registered" 
"""Username already registered

The username is already registered.
"""

USERNAME_CHANGE_FAILED_DETAIL = "Username change failed" 
"""Username change failed

The username change failed.
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

INVALID_USERNAME_OR_EMAIL_DETAIL = "Invalid username or email" 
"""Invalid username or email

The username or email is invalid.
"""

