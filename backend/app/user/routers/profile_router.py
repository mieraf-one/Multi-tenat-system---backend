from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.user.models.user import User
from app.dependencies.auth.get_current_user import get_current_user
from app.user.schemas.auth import auth_schema

from app.user.services.update.update_email import email_update
from app.user.services.update.update_password import password_update
from app.user.services.update.update_username import username_update



router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


# -------------------------------------------------------
#                       PROFILE
# -------------------------------------------------------


@router.get('/me', response_model=auth_schema.ProfileOut)
def profile_route(current_user: User = Depends(get_current_user)):
    return current_user

# -------------------------------------------------------
#                  UPDATE PASSWORD
# -------------------------------------------------------
@router.post('/update/password')
def password_update_route(data: auth_schema.PasswordUpdateIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    password_update(data=data, user_id=current_user.id, db=db)
    return {"message": "Password updated"}


# -------------------------------------------------------
#                  UPDATE EMAIL
# -------------------------------------------------------
@router.post('/update/email')
def email_update_route(data: auth_schema.EmailUpdateIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    email_update(new_email=data.email, current_user=current_user, db=db)
    return {"message": "Email updated"}


# -------------------------------------------------------
#                  UPDATE USERNAME
# -------------------------------------------------------
@router.post('/update/username')
def username_update_route(data: auth_schema.UsernameUpdateIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    username_update(new_username=data.username, current_user=current_user, db=db)
    return {"message": "Username updated"}