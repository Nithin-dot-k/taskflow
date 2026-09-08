import bcrypt

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