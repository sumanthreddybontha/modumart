import json
from app.cart.redis_client import r
from app.models.order import Order, OrderItem
from sqlalchemy.orm import Session


def add_to_cart(user_id: int, product_id: int, quantity: int):
    cart_key = f"cart:{user_id}"
    cart = r.get(cart_key)
    if cart:
        cart_items = json.loads(cart)
    else:
        cart_items = []

    # Check if product already in cart
    for item in cart_items:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            break
    else:
        cart_items.append({"product_id": product_id, "quantity": quantity})

    r.set(cart_key, json.dumps(cart_items))

def get_cart(user_id: int):
    cart_key = f"cart:{user_id}"
    cart = r.get(cart_key)
    if cart:
        return json.loads(cart)
    return []

def remove_from_cart(user_id: int, product_id: int, quantity: int):
    cart_key = f"cart:{user_id}"
    existing_cart_json = r.get(cart_key)

    if existing_cart_json is None:
        return

    cart = json.loads(existing_cart_json)
    updated_cart = []

    for item in cart:
        if item["product_id"] == product_id:
            if item["quantity"] > quantity:
                item["quantity"] -= quantity
                updated_cart.append(item)
            # If quantity equals or drops below, we skip appending (removes item)
        else:
            updated_cart.append(item)

    r.set(cart_key, json.dumps(updated_cart))

def checkout_cart(user_id: int, db: Session):
    cart_key = f"cart:{user_id}"
    cart = r.get(cart_key)
    if not cart:
        return None

    cart_items = json.loads(cart)

    order = Order(user_id=user_id)
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item["product_id"],
            quantity=item["quantity"]
        )
        db.add(order_item)

    db.commit()

    #Ensure order.items is populated
    order.items = db.query(OrderItem).filter_by(order_id=order.id).all()

    r.delete(cart_key)

    return order

