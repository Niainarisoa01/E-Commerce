from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.base import get_db
from app.schemas.order import Order, OrderCreate
from app.models.order import Order as OrderModel, OrderItem as OrderItemModel
from app.models.product import Product as ProductModel

router = APIRouter()

@router.get("/", response_model=List[Order])
async def read_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste des commandes.
    """
    orders = db.query(OrderModel).offset(skip).limit(limit).all()
    return orders

@router.get("/{order_id}", response_model=Order)
async def read_order(order_id: int, db: Session = Depends(get_db)):
    """
    Récupère une commande spécifique par son ID.
    """
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return order

@router.post("/", response_model=Order)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle commande.
    """
    # Créer la commande
    db_order = OrderModel(
        user_id=order.user_id,
        total_amount=order.total_amount,
        status=order.status
    )
    db.add(db_order)
    db.flush()  # Pour obtenir l'ID de la commande

    # Créer les items de la commande
    for item in order.items:
        # Vérifier le stock
        product = db.query(ProductModel).filter(ProductModel.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produit {item.product_id} non trouvé")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Stock insuffisant pour le produit {product.name}")

        # Créer l'item
        db_item = OrderItemModel(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price
        )
        db.add(db_item)

        # Mettre à jour le stock
        product.stock -= item.quantity

    db.commit()
    db.refresh(db_order)
    return db_order

@router.put("/{order_id}/status")
async def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """
    Met à jour le statut d'une commande.
    """
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    
    if status not in ["pending", "completed", "cancelled"]:
        raise HTTPException(status_code=400, detail="Statut invalide")
    
    order.status = status
    db.commit()
    return {"message": "Statut mis à jour avec succès"}
