import os
import httpx
import logging
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from backend.core.services import LoggingService
from .models import User
from backend.db.session import get_session
from jose import jwt

router = APIRouter()
logger = LoggingService.get_logger(__name__)

# ENV vars
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")  # change for prod

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


@router.get("/auth/login/google")
def login_with_google():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    url = httpx.URL(GOOGLE_AUTH_URL).copy_merge_params(params)
    return RedirectResponse(url)


@router.get("/auth/callback")
async def auth_callback(code: str, session: Session = Depends(get_session)):
    # Exchange code for access token
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        token_res = await client.post(GOOGLE_TOKEN_URL, data=token_data)
        if token_res.status_code != 200:
            logger.error("Failed to get token: %s", token_res.text)
            raise HTTPException(status_code=400, detail="OAuth token exchange failed")
        token_json = token_res.json()

        # Get user info
        headers = {"Authorization": f"Bearer {token_json['access_token']}"}
        userinfo_res = await client.get(GOOGLE_USERINFO_URL, headers=headers)
        if userinfo_res.status_code != 200:
            logger.error("Failed to get user info: %s", userinfo_res.text)
            raise HTTPException(status_code=400, detail="OAuth user info failed")

        userinfo = userinfo_res.json()
        email = userinfo["email"]

        # Create or fetch user
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            user = User(email=email, hashed_password="oauth")  # no real password
            session.add(user)
            session.commit()
            session.refresh(user)

    # Issue JWT
    token = jwt.encode({"sub": str(user.id)}, JWT_SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
