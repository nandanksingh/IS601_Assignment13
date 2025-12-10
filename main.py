# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: FastAPI Application Entrypoint
# File: main.py
# ----------------------------------------------------------

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles  

from app.core.config import settings
from app.database.dbase import init_db

# Routers
from app.routers.ui import router as ui_router
from app.routers.auth import router as auth_router
from app.routers.calc import router as calc_router
from app.routers.health import router as health_router


# ----------------------------------------------------------
# Create FastAPI application
# ----------------------------------------------------------
app = FastAPI(
    title="Calculations App",
    description="Web application with authentication, UI pages, and calculation routes.",
    version="1.0.0",
)

# ----------------------------------------------------------
# Static Files (CSS, JS, Images)
# ----------------------------------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")  # <--- REQUIRED


# ----------------------------------------------------------
# Logging
# ----------------------------------------------------------
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("main")


# ----------------------------------------------------------
# Templates
# ----------------------------------------------------------
templates = Jinja2Templates(directory="templates")


# ----------------------------------------------------------
# CORS Middleware
# ----------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------------------------
# Register Routers
# UI FIRST (because it defines "/")
# ----------------------------------------------------------
app.include_router(ui_router)
app.include_router(auth_router)
app.include_router(calc_router)
app.include_router(health_router)


# ----------------------------------------------------------
# Startup: Initialize database
# ----------------------------------------------------------
@app.on_event("startup")
def on_startup():
    try:
        logger.info("Initializing database...")
        init_db()
    except Exception as e:
        logger.error(f"Database initialization error: {e}")


# ----------------------------------------------------------
# Swagger Shortcut
# ----------------------------------------------------------
@app.get("/swagger", include_in_schema=False)
def swagger_redirect():
    return RedirectResponse("/docs")

