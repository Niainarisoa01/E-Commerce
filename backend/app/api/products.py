from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.base import get_db
from app.schemas.product import Product, ProductCreate
from app.models.product import Product as ProductModel

router = APIRouter()

@router.get("/", response_model=List[Product])
async def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste des produits.
    """
    products = db.query(ProductModel).filter(ProductModel.is_active == True).offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=Product)
async def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Récupère un produit spécifique par son ID.
    """
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product

@router.post("/", response_model=Product)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Crée un nouveau produit.
    """
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """
    Met à jour un produit existant.
    """
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Supprime un produit (soft delete).
    """
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    
    db_product.is_active = False
    db.commit()
    return None
