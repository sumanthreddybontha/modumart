import json
from app.cart.redis_client import r

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

def remove_from_cart(user_id: int, product_id: int):
    cart_key = f"cart:{user_id}"
    cart = r.get(cart_key)
    if not cart:
        return

    cart_items = json.loads(cart)
    cart_items = [item for item in cart_items if item["product_id"] != product_id]
    r.set(cart_key, json.dumps(cart_items))


