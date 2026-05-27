from fastapi import HTTPException, status

from app.user.models.user_model import User


def is_user_active(current_user: User):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid user'
        )