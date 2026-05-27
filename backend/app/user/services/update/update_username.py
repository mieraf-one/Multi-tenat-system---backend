from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.user.models.user_model import User

def validate_username(new_username: str, old_username: str, db: Session):
    # check old username == new username
    if old_username == new_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username are same'
        )
    
    user = db.query(User).filter(User.username==new_username).first()

    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username already used'
        )


def save_new_username(user: User, new_username: str, db: Session):
    user.username = new_username

    db.commit()

def username_update(new_username: str, current_user: User, db: Session):
    validate_username(new_username=new_username, old_username=current_user.username, db=db)
    save_new_username(user=current_user, new_username=new_username, db=db)
