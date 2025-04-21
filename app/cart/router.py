from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.user import UserResponse
from app.services.auth_utils import get_current_user
from app.cart.service import add_to_cart, get_cart, remove_from_cart, checkout_cart
from app.schemas.cart import CartItem
from app.schemas.order import OrderResponse

router = APIRouter(prefix="/cart", tags=["Cart"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_item_to_cart(item: CartItem, current_user: UserResponse = Depends(get_current_user)):
    add_to_cart(current_user.id, item.product_id, item.quantity)
    return {"message": "Item added to cart"}

@router.get("/view")
def view_cart( current_user: UserResponse = Depends(get_current_user)):
    cart = get_cart(current_user.id)
    return {"cart": cart}
   
@router.post("/remove")
def remove_item_from_cart(
    item: CartItem,
    current_user: UserResponse = Depends(get_current_user)
):
    remove_from_cart(current_user.id, item.product_id, item.quantity)
    return {"message": "Item quantity reduced or removed from cart"}


@router.post("/checkout", response_model=OrderResponse)
def checkout(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = checkout_cart(current_user.id, db)
    if not order:
        raise HTTPException(status_code=400, detail="Cart is empty")
    return order
