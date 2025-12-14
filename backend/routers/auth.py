from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import schemas, crud
from .. import dependencies
from ..dependencies import create_access_token

router = APIRouter(tags=["auth"])

# =====================================================
# REGISTER
# =====================================================

@router.post(
    "/auth/register",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(dependencies.get_db)
):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    return crud.create_user(db=db, user=user)


# =====================================================
# LOGIN
# =====================================================

@router.post(
    "/auth/login",
    response_model=schemas.Token,
    status_code=status.HTTP_200_OK
)
def login(
    credentials: schemas.LoginRequest,
    db: Session = Depends(dependencies.get_db)
):
    user = dependencies.authenticate_user(
        db,
        credentials.username,
        credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(
        data={
            "sub": user.username,
            "is_admin": user.is_admin
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
