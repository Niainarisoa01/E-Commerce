import sys
import signal
from contextlib import asynccontextmanager
sys.dont_write_bytecode = True

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.base import Base, engine, SessionLocal

# Variable globale pour le contrôle de l'arrêt
should_exit = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code à exécuter au démarrage
    print("Starting up...")
    db = SessionLocal()
    try:
        yield
    finally:
        # Code à exécuter à l'arrêt
        print("Shutting down...")
        db.close()

def signal_handler(signum, frame):
    """Gestionnaire de signal pour l'arrêt gracieux"""
    global should_exit
    print("Signal reçu, arrêt gracieux en cours...")
    should_exit = True

# Configuration du gestionnaire de signal
signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # kill ou docker stop

# Création des tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import et inclusion des routers
from app.api import auth, users

# Inclusion des routers de base
app.include_router(auth.router, prefix=settings.API_V1_STR + "/auth", tags=["auth"])
app.include_router(users.router, prefix=settings.API_V1_STR + "/users", tags=["users"])

# Import et inclusion conditionnelle des autres routers
try:
    from app.api import products, orders, cart
    app.include_router(products.router, prefix=settings.API_V1_STR + "/products", tags=["products"])
    app.include_router(orders.router, prefix=settings.API_V1_STR + "/orders", tags=["orders"])
    app.include_router(cart.router, prefix=settings.API_V1_STR + "/cart", tags=["cart"])
except ImportError:
    pass

@app.get("/health")
async def health_check():
    """Endpoint de vérification de santé"""
    if should_exit:
        return {"status": "shutting_down"}
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API E-commerce"}

if __name__ == "__main__":
    import uvicorn
    config = uvicorn.Config(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        timeout_graceful_shutdown=10,
        loop="asyncio"
    )
    server = uvicorn.Server(config)
    server.run()
