from app.user.models.user import User
from sqlalchemy.orm import Session

def delete_user(current_user: User, db: Session):
    current_user.is_active = False
    current_user.refresh_tokens.clear()
    db.commit()