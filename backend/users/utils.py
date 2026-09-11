from datetime import datetime, timedelta, timezone
import jwt
import bcrypt
from config import settings


def hash_password(password: str) -> str:
    """
    Convert a plain-text password into a secure hash.
    """
    # 1. Convert the plain text string into raw bytes
    password_bytes = password.encode('utf-8')
    
    # 2. Generate a random "salt" (extra security noise)
    salt = bcrypt.gensalt()
    
    # 3. Hash the password with the salt and return the decoded string
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if a typed password matches the stored hash.
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    
    # Check if the plain password matches the hash
    return bcrypt.checkpw(password_bytes, hashed_bytes)


# --- NEW JWT FUNCTIONS BELOW ---

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Generate a secure, signed JWT access token.
    """
    to_encode = data.copy()
    
    # 1. Set the expiration date (default to 15 minutes if not specified)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        
    # 2. Add the 'exp' claim to the data payload
    to_encode.update({"exp": expire})
    
    # 3. Sign the token using our secret key and return the token string
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt