# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: UI Route Handlers
# File: app/routers/ui.py
# ----------------------------------------------------------
# Description:
# Routes for rendering front-end HTML templates using Jinja2.
# These endpoints serve:
#   • Public homepage (/)
#   • Login page
#   • Registration page
#   • Dashboard (JWT-protected via JS redirect)
#   • Logout confirmation screen
#
# UI is kept separate from API routes for clean architecture.
# ----------------------------------------------------------

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["UI Pages"])
templates = Jinja2Templates(directory="templates")


# ----------------------------------------------------------
# Public Homepage
# ----------------------------------------------------------
@router.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ----------------------------------------------------------
# Login Page
# ----------------------------------------------------------
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# ----------------------------------------------------------
# Registration Page
# ----------------------------------------------------------
@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# ----------------------------------------------------------
# Dashboard Page
# ----------------------------------------------------------
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    """
    The dashboard requires token validation on the frontend.
    If no token exists in localStorage, dashboard.html JS will
    automatically redirect the user back to /login.
    """
    return templates.TemplateResponse("dashboard.html", {"request": request})


# ----------------------------------------------------------
# Logout Page — FRONTEND ONLY
# ----------------------------------------------------------
@router.get("/logout", response_class=HTMLResponse)
def logout_page(request: Request):
    """
    This route displays the logout page.
    The logout.html template clears localStorage and redirects.
    """
    return templates.TemplateResponse("logout.html", {"request": request})
