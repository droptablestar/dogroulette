import os

from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from sqlmodel import Session, select

from backend.db.session import get_session
from .models import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)  # tokenUrl is required but not used here


class AuthService:
    JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")

    @classmethod
    def get_current_user(
        cls,
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session),
    ) -> User:
        payload = cls.decode_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=400, detail="Missing user ID")

        user = session.exec(select(User).where(User.id == int(user_id))).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    @classmethod
    def decode_token(cls, token: str) -> dict:
        try:
            payload = jwt.decode(token, cls.JWT_SECRET, algorithms=["HS256"])
            return payload
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid"
            )
