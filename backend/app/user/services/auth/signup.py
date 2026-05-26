from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.user.models.user import User
from app.user.schemas.auth.auth_schema import SignupIn

# check email exists before
def is_email_before(email: str, db: Session) -> bool:
    fetched_email = db.query(User).filter(User.email==email).first()
    
    if fetched_email is None:
        return False
    
    return True

# check username exists before
def is_username_before(username: str, db: Session) -> bool:
    fetched_username = db.query(User).filter(User.username==username).first()
    
    if fetched_username is None:
        return False
    
    return True

# save user to db
def save_create_user(data: SignupIn, db: Session):
    # remove confirm_password
    user_data: dict = data.model_dump(exclude={'confirm_password'})

    # change password to hashed_password
    user_data['hashed_password'] = hash_password(user_data.pop('password'))

    new_user = User(**user_data)

    # save to db
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# create user
def create_user(data: SignupIn, db: Session):
    # check email before
    if is_email_before(data.email, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already exists'
        )
    
    # check username before
    if is_username_before(data.username, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username already exists'
        )
    
    # save user in db
    return save_create_user(data, db)
