import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost:5432/inventory_db")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(title="Product Service")

class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)

Base.metadata.create_all(bind=engine)

class ProductCreate(BaseModel):
    name: str
    quantity: int = 0

class ProductOut(BaseModel):
    id: int
    name: str
    quantity: int
    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products", response_model=ProductOut)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    existing = db.query(ProductModel).filter(ProductModel.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product with this name already exists")
    p = ProductModel(name=payload.name, quantity=payload.quantity)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@app.get("/products", response_model=List[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()

@app.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    p = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p
