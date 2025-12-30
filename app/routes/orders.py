from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import SessionLocal
from app import models
from app.schemas import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate
)
from app.utils.status_validator import is_valid_transition

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# -------------------------------------------------
# Database Dependency
# -------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------------
# STEP 4: Create Order
# -------------------------------------------------
@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    new_order = models.Order(
        customer_name=order.customer_name,
        customer_contact=order.customer_contact,
        merchant_ref=order.merchant_ref,
        current_status="created"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


# -------------------------------------------------
# Get Order by ID (Current State)
# -------------------------------------------------
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


# -------------------------------------------------
# STEP 5: Update Order Status + History
# -------------------------------------------------
@router.patch("/{order_id}/status")
def update_order_status(
    order_id: str,
    update: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Validate status transition
    if not is_valid_transition(order.current_status, update.new_status):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from {order.current_status} to {update.new_status}"
        )

    # Update order state
    order.current_status = update.new_status
    order.updated_at = datetime.utcnow()
    order.version += 1

    # Save immutable history
    history = models.OrderStatusHistory(
        order_id=order.id,
        status=update.new_status,
        source=update.source
    )

    db.add(history)
    db.commit()
    db.refresh(order)

    return {
        "order_id": order.id,
        "new_status": order.current_status,
        "updated_at": order.updated_at
    }


# -------------------------------------------------
# STEP 6: Get Active Orders (Current Snapshot)
# -------------------------------------------------
@router.get("/")
def get_active_orders(db: Session = Depends(get_db)):
    orders = (
        db.query(models.Order)
        .filter(models.Order.current_status != "delivered")
        .all()
    )

    return [
        {
            "order_id": o.id,
            "status": o.current_status,
            "updated_at": o.updated_at
        }
        for o in orders
    ]


# -------------------------------------------------
# STEP 6: Get Full Status History
# -------------------------------------------------
@router.get("/{order_id}/history")
def get_order_history(order_id: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    history = (
        db.query(models.OrderStatusHistory)
        .filter(models.OrderStatusHistory.order_id == order_id)
        .order_by(models.OrderStatusHistory.timestamp)
        .all()
    )

    return [
        {
            "status": h.status,
            "source": h.source,
            "timestamp": h.timestamp
        }
        for h in history
    ]
