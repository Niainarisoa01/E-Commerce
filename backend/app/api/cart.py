from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal

from app.db.base import get_db
from app.schemas.cart import Cart, CartCreate, CartItem, CartItemCreate
from app.models.cart import Cart as CartModel, CartItem as CartItemModel
from app.models.product import Product as ProductModel

router = APIRouter()

@router.get("/", response_model=Cart)
async def read_cart(user_id: int, db: Session = Depends(get_db)):
    """
    Récupère le panier d'un utilisateur.
    """
    cart = db.query(CartModel).filter(CartModel.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Panier non trouvé")
    return cart

@router.post("/items", response_model=CartItem)
async def add_cart_item(
    user_id: int,
    item: CartItemCreate,
    db: Session = Depends(get_db)
):
    """
    Ajoute un article au panier.
    """
    # Vérifier si le produit existe
    product = db.query(ProductModel).filter(ProductModel.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    # Vérifier le stock
    if product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Stock insuffisant")

    # Récupérer ou créer le panier
    cart = db.query(CartModel).filter(CartModel.user_id == user_id).first()
    if not cart:
        cart = CartModel(user_id=user_id)
        db.add(cart)
        db.flush()

    # Vérifier si l'article existe déjà dans le panier
    cart_item = db.query(CartItemModel).filter(
        CartItemModel.cart_id == cart.id,
        CartItemModel.product_id == item.product_id
    ).first()

    if cart_item:
        # Mettre à jour la quantité
        cart_item.quantity += item.quantity
    else:
        # Créer un nouvel article
        cart_item = CartItemModel(
            cart_id=cart.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price
        )
        db.add(cart_item)

    # Mettre à jour le montant total
    cart.total_amount += Decimal(str(product.price)) * item.quantity

    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.delete("/items/{item_id}")
async def remove_cart_item(
    user_id: int,
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprime un article du panier.
    """
    cart = db.query(CartModel).filter(CartModel.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Panier non trouvé")

    cart_item = db.query(CartItemModel).filter(
        CartItemModel.id == item_id,
        CartItemModel.cart_id == cart.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Article non trouvé dans le panier")

    # Mettre à jour le montant total
    cart.total_amount -= Decimal(str(cart_item.unit_price)) * cart_item.quantity

    db.delete(cart_item)
    db.commit()
    return {"message": "Article supprimé du panier"}

@router.put("/items/{item_id}")
async def update_cart_item(
    user_id: int,
    item_id: int,
    quantity: int,
    db: Session = Depends(get_db)
):
    """
    Met à jour la quantité d'un article dans le panier.
    """
    if quantity < 1:
        raise HTTPException(status_code=400, detail="La quantité doit être supérieure à 0")

    cart = db.query(CartModel).filter(CartModel.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Panier non trouvé")

    cart_item = db.query(CartItemModel).filter(
        CartItemModel.id == item_id,
        CartItemModel.cart_id == cart.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Article non trouvé dans le panier")

    # Vérifier le stock
    product = db.query(ProductModel).filter(ProductModel.id == cart_item.product_id).first()
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="Stock insuffisant")

    # Mettre à jour le montant total
    cart.total_amount -= Decimal(str(cart_item.unit_price)) * cart_item.quantity
    cart.total_amount += Decimal(str(cart_item.unit_price)) * quantity

    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item
