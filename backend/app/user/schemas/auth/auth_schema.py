from pydantic import BaseModel, field_validator, model_validator, EmailStr
from datetime import datetime

class SignupIn(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def validate_pwd(self):
        if self.password != self.confirm_password:
            raise ValueError('passwords do not match')
        
        return self


class SignupOut(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LoginIn(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str

    @model_validator(mode='after')
    def validate_username_or_email_exists(self):
        if self.username is None and self.email is None:
            raise ValueError('Enter username or email')
        
        return self
    
class LoginOut(BaseModel):
    access_token: str | None
    refresh_token: str | None


class ProfileOut(SignupOut):
    pass


class EmailCodeIn(BaseModel):
    code: str

    @field_validator('code')
    @classmethod
    def validate_code(cls, value):
        if len(value) != 5 or not value.isdigit():
            raise ValueError('Code must be exactly 5 digits')
        
        return value
    
class PasswordUpdateIn(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

    @model_validator(mode='after')
    def validate_passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError('Passwords do not match')
        
        if self.old_password == self.new_password:
            raise ValueError('same password from old')
        
        return self


class EmailUpdateIn(BaseModel):
    email: EmailStr


class UsernameUpdateIn(BaseModel):
    username: str


class RefreshToken(BaseModel):
    refresh_token: str

class ResetPasswordUpdateIn(BaseModel):
    code: str
    new_password: str
    confirm_password: str

    @model_validator(mode='after')
    def validate_passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError('Passwords do not match')
        
        return self