from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from sqlalchemy.orm import Session
from users.models import UserModel
from core.database import get_db
from core.config import settings
from datetime import datetime,timedelta,timezone
from jwt.exceptions import DecodeError,InvalidSignatureError
import jwt


security = HTTPBearer()


def generate_access_token(user_id: int, expires_in: int= 60*5) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "type": "access",
        "user_id": user_id,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in)
    }
    
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")


def generate_refresh_token(user_id: int, expires_in: int= 3600*24) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "type": "refresh",
        "user_id": user_id,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in)
    }
    
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")


def get_auth_username(
    credentials: HTTPAuthorizationCredentials=Depends(security),
    db: Session=Depends(get_db)
):
    token = credentials.credentials
    try:
        decode = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        user_id = decode.get("user_id", None)
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentication failed, user_id not in the payload.")
        if decode.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentication failed, token type not valid.")
        if datetime.now() > datetime.fromtimestamp(decode.get("exp")):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentication failed, token expired.")

        user_obj = db.query(UserModel).filter_by(id=user_id).one()
        return user_obj

    except InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentication failed, invalid signature.")
    except DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentication failed, decode faild.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Authentication failed,{e}.")


def decode_refresh_token(token):
    try:
        decode = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        user_id = decode.get("user_id", None)
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="user_id not in the payload.")
            
        if decode.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="token type not valid.")
        
        if datetime.now() > datetime.fromtimestamp(decode.get("exp")):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="token expired.")
        return user_id        
        
    except InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid signature.")
    except DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="decode faild.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"{e}.")
