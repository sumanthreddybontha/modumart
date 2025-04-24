from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.order import Order
from app.models.user import User
from app.schemas.order import OrderResponse
from app.services.auth_utils import get_current_user
from app.services.auth_utils import require_admin
from typing import List


router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/all", response_model=List[OrderResponse])
def get_all_orders(db: Session = Depends(get_db), current_admin: User = Depends(require_admin)):
    orders = db.query(Order).all()
    return orders

@router.get("/history", response_model=List[OrderResponse])
def get_order_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order











