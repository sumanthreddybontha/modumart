from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse
from app.services.auth_utils import get_current_user
from app.cart.schemas import CartItem
from pydantic import BaseModel
from app.cart.service import add_to_cart, get_cart, remove_from_cart


router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/add")
def add_item_to_cart(item: CartItem, current_user: UserResponse = Depends(get_current_user)):
    add_to_cart(user_id=current_user.id, product_id=item.product_id, quantity=item.quantity)
    return {"message": "Item added to cart"}

@router.get("/view")
def view_cart(current_user: UserResponse = Depends(get_current_user)):
    cart = get_cart(current_user.id)
    return {"cart": cart}

class RemoveRequest(BaseModel):
    product_id: int

@router.post("/remove")
def remove_item_from_cart(req: RemoveRequest, current_user: UserResponse = Depends(get_current_user)):
    remove_from_cart(current_user.id, req.product_id)
    return {"message": "Item removed from cart"}


