from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from app.core.security import hash_password, verify_password
from app.user.services.verifications.send_email_verification import email_message, generate_code, save_code_to_db, conf
from fastapi_mail import FastMail
from app.user.models.verification_code import EmailVerificationCode
from app.user.models.user import User
from sqlalchemy.orm import Session


# --------------------------------------------------------------
#                   SEND RESET CODE
# --------------------------------------------------------------

def waits_before_sending_again(current_user: User):
    # sent codes
    codes = current_user.sent_codes

    # check created_at + 1 minutes before sending again
    if codes and codes[0].created_at + timedelta(minutes=1) > datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Please try again in 1 minute."
        )  


async def send_code(email: str):
    gen_code = str(generate_code())
    msg = email_message(
        subject='Reset code',
        email=email,
        body=f'Your code is: {gen_code}'
    )

    try:
        await FastMail(conf).send_message(msg)
        return gen_code
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to send reset email'
        )


async def send_reset_code(current_user: User, db: Session):
    waits_before_sending_again(current_user=current_user)
    code = await send_code(email=current_user.email)
    save_code_to_db(code=code, user_id=current_user.id, db=db)



# --------------------------------------------------------------
#               VERIFY AND UPDATE PASSWORD
# --------------------------------------------------------------
# verify reset code
def verify_reset_code(code: str, user_id: int, db: Session):
    db_code = (
        db.query(EmailVerificationCode)
            .filter(
                EmailVerificationCode.code==code,
                EmailVerificationCode.user_id==user_id)
            .first()
    )


    if db_code is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid code'
        )
    

    if db_code.is_used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid code'
        )
    
    if db_code.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Expired code'
        )
    
    return db_code
    


def validate_password(old_password: str, new_password: str):
    if verify_password(new_password, old_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='same password'
        )


# save new password
def save_new_password(current_user: User, code: EmailVerificationCode, new_password: str, db: Session):
    current_user.hashed_password = hash_password(new_password)
    code.is_used = True

    db.commit()


def update_reset_password(code: str, new_password: str, current_user: User, db: Session):
    validate_password(old_password=current_user.hashed_password, new_password=new_password)
    db_code = verify_reset_code(code=code, user_id=current_user.id, db=db)
    save_new_password(current_user=current_user, new_password=new_password, code=db_code, db=db)
