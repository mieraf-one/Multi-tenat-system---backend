from fastapi import HTTPException, status
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from sqlalchemy.orm import Session

import random
from datetime import datetime, timedelta, timezone

from app.user.models.verification_code_model import EmailVerificationCode
from app.user.models.user_model import User
from app.core.config import settings


# Connection Configuration
conf = ConnectionConfig(
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = 587,
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False
)

# Generate 5-digits code
def generate_code():
    return random.randint(10000, 99999)


# save code to db
def save_code_to_db(code: str, user_id, db: Session, expires_at: timedelta = timedelta(minutes=15)):
    data = {
        'code': code,
        'user_id': user_id,
        'expires_at': datetime.now(timezone.utc) + expires_at
    }

    new_code = EmailVerificationCode(**data)

    db.add(new_code)
    db.commit()
    db.refresh(new_code)

    return new_code

# message
def email_message(subject, email, body):
    msg = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype=MessageType.plain
    )
    return msg


def validate_user(user_id, db: Session) -> None:
    '''
    Check user is verified.

    Waits 1 minutes before sending again.
    '''
    user = db.query(User).filter(User.id==user_id).first()

    # check user existance
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid user'
        )
    
    # check if user already verified
    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='already verified'
        )
    
    # sent codes
    codes = user.sent_codes

    # check created_at + 1 minutes before sending again
    if codes and codes[0].created_at + timedelta(minutes=1) > datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Please try again in 1 minute."
        )    


# send code
async def send_code(email: str, user_id, db: Session):
    # check if user verified before
    # waits 1 minute before sending again
    validate_user(user_id=user_id, db=db)

    # generate code
    gen_code = str(generate_code())

    # generate message
    msg = email_message(
        subject='Verify your email',
        email=email,
        body=f'Your code is: {gen_code}'
    )


    try:
        # send verification email
        await FastMail(conf).send_message(msg)

        # save code in db
        return save_code_to_db(gen_code, user_id, db)
    except Exception:
        # rollback if error happens
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to send Verification email'
        )
