from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_


from app.core.security import create_access_token, create_refresh_token, verify_password
from app.user.models.user_model import User
from app.user.schemas.auth.auth_schema import LoginIn


from app.user.services.validators.is_user_active import is_user_active

# validate user
def validate_user(data: LoginIn, db: Session):
    credential = (
        db.query(User)
            .filter(
                or_(
                    User.email==data.email,
                    User.username==data.username
                    ))
            .first()
    )

    # check user existance
    if credential is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Login Information. 1'
        )
    
    # validate password
    if not verify_password(data.password, credential.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Login Information. 2'
        )
    
    is_user_active(current_user=credential)
    
    return credential.id


def login_user(data: LoginIn, db: Session):
    # valiate user existance and password match
    user_id = validate_user(data=data, db=db)

    # create access token
    access_token = create_access_token({'user_id': user_id})

    # create refresh token
    refresh_token = create_refresh_token({'user_id': user_id}, db=db)

    return {'access_token': access_token, 'refresh_token': refresh_token}