from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    """Hashes a password using bcrypt.

    Args:
        password: A string representing the plain-text password to hash.

    Returns:
        A string representing the hashed password.
    """
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    """Verifies a plain-text password against a hashed password.

    Args:
        plain_password: A string representing the plain-text password to verify.
        hashed_password: A string representing the hashed password to compare against.

    Returns:
        True if the plain password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)