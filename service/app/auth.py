from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext


SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Usuario fake (luego esto sería DB)
fake_users = [
    {
        "username": "admin",
        "hashed_password": "$pbkdf2-sha256$29000$YizFGKNUyrm3tlYK4fw/Jw$F/9uFVNhZ8V3HUUw2h/b/KIDU.e5NsnpuNwj.uYFEuQ",
        "role": "admin"
    },
    {
        "username": "sebastian",
        "hashed_password": "$pbkdf2-sha256$29000$YizFGKNUyrm3tlYK4fw/Jw$F/9uFVNhZ8V3HUUw2h/b/KIDU.e5NsnpuNwj.uYFEuQ",
        "role": "user"
    },
    {
        "username": "juan",
        "hashed_password": "$pbkdf2-sha256$29000$YizFGKNUyrm3tlYK4fw/Jw$F/9uFVNhZ8V3HUUw2h/b/KIDU.e5NsnpuNwj.uYFEuQ",
        "role": "user"
    }
]
def get_current_user_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")
        role = payload.get("role")

        if username is None:
            raise Exception("Invalid token")

        return {
            "username": username,
            "role": role
        }

    except JWTError:
        raise Exception("Invalid token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str):
    return next(
        (user for user in fake_users if user["username"] == username),
        None
    )


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None

    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)