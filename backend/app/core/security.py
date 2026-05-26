from sqlalchemy.orm import Session

from datetime import datetime, timedelta, timezone
from jose import jwt
import bcrypt

from app.user.models.token import RefreshToken
from app.core.config import settings



# hash pwd
def hash_password(pwd: str) -> str:
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()


# verify password - plain and hashed pwd
def verify_password(plain_pwd: str, hashed_pwd: str):
    return bcrypt.checkpw(plain_pwd.encode(), hashed_pwd.encode())

# create access token
def create_access_token(data: dict, expires_at: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    to_encode['exp'] = datetime.now(timezone.utc) + expires_at

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm='HS256')

# create refresh token
def create_refresh_token(data: dict, db: Session, expires_at: timedelta = timedelta(days=7)):
    new_token = create_access_token(data, expires_at)
    save_refresh_token(user_id=data.get('user_id'), token=new_token, expires_at=datetime.now(timezone.utc) + expires_at, db=db)
    return new_token

def save_refresh_token(user_id, token, expires_at, db: Session):
    data = {
        'user_id': user_id,
        'token': token,
        'expires_at': expires_at
    }

    save = RefreshToken(**data)

    db.add(save)
    db.commit()