from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =====================================================
# PASSWORD UTILS
# =====================================================

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# =====================================================
# USER CRUD
# =====================================================

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# =====================================================
# SWEET CRUD
# =====================================================

def get_sweets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sweet).offset(skip).limit(limit).all()


def create_sweet(db: Session, sweet: schemas.SweetCreate):
    db_sweet = models.Sweet(
        name=sweet.name,
        category=sweet.category,
        price=sweet.price,
        quantity=sweet.quantity
    )
    db.add(db_sweet)
    db.commit()
    db.refresh(db_sweet)
    return db_sweet


def update_sweet(db: Session, sweet_id: int, sweet: schemas.SweetCreate):
    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not db_sweet:
        return None

    db_sweet.name = sweet.name
    db_sweet.category = sweet.category
    db_sweet.price = sweet.price
    db_sweet.quantity = sweet.quantity

    db.commit()
    db.refresh(db_sweet)
    return db_sweet


def delete_sweet(db: Session, sweet_id: int):
    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not db_sweet:
        return None

    db.delete(db_sweet)
    db.commit()
    return db_sweet

def purchase_sweet(db: Session, sweet_id: int):
    sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not sweet:
        return None

    if sweet.quantity <= 0:
        return "OUT_OF_STOCK"

    sweet.quantity -= 1
    db.commit()
    db.refresh(sweet)
    return sweet


def restock_sweet(db: Session, sweet_id: int, amount: int):
    sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not sweet:
        return None

    sweet.quantity += amount
    db.commit()
    db.refresh(sweet)
    return sweet
# =====================================================
# SEARCH SWEETS
# =====================================================

def search_sweets(
    db: Session,
    name: str | None = None,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
):
    query = db.query(models.Sweet)

    if name:
        query = query.filter(models.Sweet.name.ilike(f"%{name}%"))

    if category:
        query = query.filter(models.Sweet.category.ilike(f"%{category}%"))

    if min_price is not None:
        query = query.filter(models.Sweet.price >= min_price)

    if max_price is not None:
        query = query.filter(models.Sweet.price <= max_price)

    return query.all()
