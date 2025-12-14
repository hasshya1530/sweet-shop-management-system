from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from ..database import schemas, crud
from ..dependencies import get_db, get_current_user
from ..database.models import User

router = APIRouter(tags=["sweets"])

# =====================================================
# SEARCH SWEETS (PUBLIC)  ✅ MUST BE FIRST
# =====================================================

@router.get(
    "/sweets/search",
    response_model=list[schemas.Sweet],
    status_code=status.HTTP_200_OK
)
def search_sweets(
    name: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db),
):
    return crud.search_sweets(
        db=db,
        name=name,
        category=category,
        min_price=min_price,
        max_price=max_price,
    )

# =====================================================
# CREATE SWEET (PROTECTED)
# =====================================================

@router.post(
    "/sweets/",
    response_model=schemas.Sweet,
    status_code=status.HTTP_201_CREATED
)
def create_sweet(
    sweet: schemas.SweetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if sweet.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Price must be greater than zero"
        )

    if sweet.quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity cannot be negative"
        )

    return crud.create_sweet(db=db, sweet=sweet)

# =====================================================
# READ SWEETS (PUBLIC)
# =====================================================

@router.get(
    "/sweets/",
    response_model=list[schemas.Sweet],
    status_code=status.HTTP_200_OK
)
def read_sweets(db: Session = Depends(get_db)):
    return crud.get_sweets(db=db)

# =====================================================
# UPDATE SWEET (PROTECTED)
# =====================================================

@router.put(
    "/sweets/{sweet_id}",
    response_model=schemas.Sweet,
    status_code=status.HTTP_200_OK
)
def update_sweet(
    sweet_id: int,
    sweet: schemas.SweetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated = crud.update_sweet(db, sweet_id, sweet)
    if not updated:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return updated

# =====================================================
# DELETE SWEET (ADMIN ONLY)
# =====================================================

@router.delete(
    "/sweets/{sweet_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    deleted = crud.delete_sweet(db, sweet_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sweet not found")

# =====================================================
# PURCHASE SWEET (PROTECTED)
# =====================================================

@router.post(
    "/sweets/{sweet_id}/purchase",
    response_model=schemas.Sweet,
    status_code=status.HTTP_200_OK
)
def purchase_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = crud.purchase_sweet(db, sweet_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Sweet not found")

    if result == "OUT_OF_STOCK":
        raise HTTPException(status_code=400, detail="Sweet is out of stock")

    return result

# =====================================================
# RESTOCK SWEET (ADMIN ONLY)
# =====================================================

@router.post(
    "/sweets/{sweet_id}/restock",
    response_model=schemas.Sweet,
    status_code=status.HTTP_200_OK
)
def restock_sweet(
    sweet_id: int,
    amount: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restock amount must be positive"
        )

    sweet = crud.restock_sweet(db, sweet_id, amount)
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    return sweet
