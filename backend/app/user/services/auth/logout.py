from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.user.models.token import RefreshToken
from app.user.models.user import User



def validate_token(refresh_token: str, current_user: User, db: Session):
    token = (
        db.query(RefreshToken)
            .filter(
                RefreshToken.token==refresh_token,
                RefreshToken.user_id==current_user.id)
            .first()
    )

    # check if token is exists
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid token'
        )
    
    return token


# logout user: delete token
def delete_token(refresh_token: RefreshToken, db: Session):
    db.delete(refresh_token)
    db.commit()


# logout user
def logout_user(refresh_token: str, current_user: User, db: Session):
    token = validate_token(refresh_token=refresh_token, current_user=current_user, db=db)
    delete_token(refresh_token=token, db=db)
