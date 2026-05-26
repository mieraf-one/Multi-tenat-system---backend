from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth.get_current_user import get_current_user
from app.core.database import get_db
from app.user.services.verifications.send_email_verification import send_code
from app.user.services.verifications.verify_email_verification import verify_code
from app.user.schemas.auth import auth_schema


router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


# -------------------------------------------------------
#                SEND VERIFICATION CODE
# -------------------------------------------------------
@router.post('/send-code')
async def send_code_route(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    await send_code(current_user.email, current_user.id, db=db)
    return {'message': 'Code sent'}



# -------------------------------------------------------
#                  VERIFY EMAIL CODE
# -------------------------------------------------------
@router.post('/verify')
def verify_code_route(data: auth_schema.EmailCodeIn, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_code(code=data.code, user_id=current_user.id, db=db)
    return {"message": "Successfully verified"}

