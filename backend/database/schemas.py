from pydantic import BaseModel
from typing import Optional

# ================= USER SCHEMAS =================

class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


# ================= AUTH SCHEMAS =================

class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# ================= SWEET SCHEMAS =================

class SweetBase(BaseModel):
    name: str
    category: str
    price: float
    quantity: int


class SweetCreate(SweetBase):
    pass


class Sweet(SweetBase):
    id: int

    class Config:
        orm_mode = True
