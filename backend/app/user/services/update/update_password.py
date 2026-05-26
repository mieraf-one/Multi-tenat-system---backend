from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.security import hash_password, verify_password
from app.user.models.user import User
from app.user.schemas.auth.auth_schema import PasswordUpdateIn


def validate_password(data: PasswordUpdateIn, user_id: int, db: Session):
    user = db.query(User).filter(User.id==user_id).first()

    # check user existance
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid user'
        )
    
    if not verify_password(data.old_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect old password'
        )
    
    return user


def save_new_password(user: User, new_password: str, db: Session):
    # hash new password
    user.hashed_password = hash_password(new_password)

    # remove all refresh tokens
    user.refresh_tokens.clear()
    
    db.commit()


def password_update(data: PasswordUpdateIn, user_id: int, db: Session):
    user = validate_password(data=data, user_id=user_id, db=db)
    save_new_password(user=user, new_password=data.new_password, db=db)