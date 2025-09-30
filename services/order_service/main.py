import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from typing import List

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost:5432/inventory_db")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(title="Order Service")

# -------------------
# MODELS
# -------------------
class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)


class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    product = relationship("ProductModel")


Base.metadata.create_all(bind=engine)

# -------------------
# SCHEMAS
# -------------------
class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


# -------------------
# DEPENDENCY
# -------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------
# API ROUTES
# -------------------
@app.post("/orders", response_model=OrderOut)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    # Fetch product
    product = db.query(ProductModel).filter(ProductModel.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check stock
    if product.quantity < payload.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Reduce stock
    product.quantity -= payload.quantity

    # Create order
    order = OrderModel(user_id=payload.user_id, product_id=payload.product_id, quantity=payload.quantity)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@app.get("/orders", response_model=List[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return db.query(OrderModel).all()


@app.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    o = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Order not found")
    return o
