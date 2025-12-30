from fastapi import FastAPI
from app.database import engine
from app import models

# Import routers
from app.routes.orders import router as orders_router
from app.routes.websocket import router as websocket_router

# Create DB tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Live Order Tracking System",
    version="0.1.0"
)

# Register REST routes
app.include_router(orders_router)

# Register WebSocket routes
app.include_router(websocket_router)


# Health check
@app.get("/")
def health_check():
    return {"status": "Live Order Tracking API running"}
