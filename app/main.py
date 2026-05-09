from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text

from app.core.settings import settings
from app.core.database import Base, engine
from app.api.auth_router import router as auth_router
from app.api.user_router import router as user_router
from app.api.url_router import router as url_router
from app.api.redirect import router as redirect_router

from app.models import user, url

app = FastAPI(title="Shorty", version="1.0.0", description="Encurtador de url!")


@app.get("/health")
def health():
    return {"status": "ok"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(url_router)
app.include_router(redirect_router)


Base.metadata.create_all(bind=engine)
