from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException, status

from app.user.models.verification_code import EmailVerificationCode
from app.user.models.user import User


def validate_code_from_db(code: str, user_id, db: Session):
    db_code = (
        db.query(EmailVerificationCode)
            .filter(
                EmailVerificationCode.code==code,
                EmailVerificationCode.user_id==user_id)
            .order_by(desc(EmailVerificationCode.created_at))
            .first()
        )

    # check if code exists
    if db_code is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid code'
        )

    
    # check code not used again
    if db_code.is_used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Code already used'
        )

    # validate expiration time
    if datetime.now(timezone.utc) > db_code.expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Code expired'
        )


    # update is_used to True
    db_code.is_used = True
    db_code.user.is_verified = True

    # save db
    db.commit()

def verify_code(code: str, user_id, db: Session):
    validate_code_from_db(code=code, user_id=user_id, db=db)