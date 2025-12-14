from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

from backend.routers import auth, sweets
from backend.database import models
from backend.database.database import engine, SessionLocal
from backend.database.crud import get_password_hash
from backend.dependencies import get_db

# =========================================================
# CREATE DATABASE TABLES
# =========================================================
models.Base.metadata.create_all(bind=engine)

# =========================================================
# FASTAPI APP
# =========================================================
app = FastAPI(title="Sweet Shop Management System")

# =========================================================
# CREATE DEFAULT ADMIN (ON STARTUP)
# =========================================================
def create_default_admin():
    db = SessionLocal()
    try:
        admin = db.query(models.User).filter(
            models.User.username == "admin"
        ).first()

        if not admin:
            admin_user = models.User(
                username="admin",
                hashed_password=get_password_hash("admin123"),
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Default admin created: admin / admin123")
        else:
            print("ℹ️ Admin already exists")
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    create_default_admin()

# =========================================================
# CORS CONFIGURATION
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ fine for demo / assignment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# ROUTERS
# =========================================================
API_PREFIX = "/api/v1"
app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(sweets.router, prefix=API_PREFIX)

# =========================================================
# HEALTH CHECKS
# =========================================================
@app.get("/")
def read_root():
    return {"status": "Sweet Shop Backend is Running"}

@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        db.query(models.User).first()
        return {"status": "Database connection successful"}
    except Exception as e:
        return {"status": "Database connection failed", "detail": str(e)}
