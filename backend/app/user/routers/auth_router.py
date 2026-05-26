from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session


from app.core.database import get_db
from app.user.models.user import User
from app.user.schemas.auth import auth_schema
from app.user.services.auth import delete_user
from app.user.services.auth.login import login_user
from app.user.services.auth.logout import logout_user
from app.user.services.auth.signup import create_user
from app.dependencies.auth.get_current_user import get_current_user
from app.user.services.auth.refresh_token import refresh_access_token
from app.user.services.auth.forgot_password import send_reset_code, update_reset_password



router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

# -------------------------------------------------------
#                       SIGN UP
# -------------------------------------------------------
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=auth_schema.SignupOut)
def signup_route(data: auth_schema.SignupIn, db: Session = Depends(get_db)):
    return create_user(data, db)


# -------------------------------------------------------
#                       LOGIN
# -------------------------------------------------------
@router.post('/login', response_model=auth_schema.LoginOut)
def login_route(data: auth_schema.LoginIn, db: Session = Depends(get_db)):
    return login_user(data=data, db=db)


# -------------------------------------------------------
#                      LOG OUT
# -------------------------------------------------------
@router.delete('/logout')
def logout_route(data: auth_schema.RefreshToken, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    logout_user(refresh_token=data.refresh_token, current_user=current_user, db=db)
    return {"message": "logged out"}




# -------------------------------------------------------
#              REFRESH ACCESS TOKEN
# -------------------------------------------------------
@router.post('/refresh', response_model=auth_schema.LoginOut)
def refresh_access_token_route(data: auth_schema.RefreshToken, db: Session = Depends(get_db)):
    return refresh_access_token(refresh_token=data.refresh_token, db=db)



# -------------------------------------------------------
#                 FORGOT PASSWORD
# -------------------------------------------------------

# send reset code
@router.post('/reset-code')
async def send_reset_code_route(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    await send_reset_code(current_user=current_user, db=db)
    return {"message": "reset code sent"}


# verify and change
@router.post('/forgot-password')
def forgot_password_route(data: auth_schema.ResetPasswordUpdateIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    update_reset_password(code=data.code, new_password=data.new_password, current_user=current_user, db=db)
    return {"message": "password updated"}


# -------------------------------------------------------
#                 DELETE ACCOUNT
# -------------------------------------------------------
@router.delete('/delete-account')
def delete_account_route(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    delete_user(current_user=current_user, db=db)
    return {"message": "Account deleted"}
