from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.user.models.user import User

def validate_email(new_email: str, old_email: str, db: Session):
    # check if username is same
    if old_email == new_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Emails are same'
        )
    

    user = db.query(User).filter(User.email==new_email).first()

    # check if username is exists
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already used'
        )
    


def save_new_email(user: User, new_email: str, db: Session):
    user.email = new_email
    user.is_verified = False

    db.commit()

def email_update(new_email: str, current_user: User, db: Session):
    validate_email(new_email=new_email, old_email=current_user.email, db=db)
    save_new_email(user=current_user, new_email=new_email, db=db)
