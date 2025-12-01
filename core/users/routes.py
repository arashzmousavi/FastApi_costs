from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from users.models import UserModel
from users.schemas import *
from sqlalchemy.orm import Session
from core.database import get_db
from auth.jwt_auth import *
from i18n.translator import get_locale_lang, get_translator

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def user_register(
    request: UserRegisterSchema,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale_lang),
):
    exist_user = (
        db.query(UserModel)
        .filter_by(username=request.username.lower())
        .first()
    )
    _ = get_translator(locale)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=_("user_not_found")
        )
    user_obj = UserModel(username=request.username.lower())
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return JSONResponse(content={"detail": _("welcome_message")})


@router.post("/login")
async def user_login(
    request: UserLoginSchema,
    response: Response,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale_lang),
):
    user_obj = (
        db.query(UserModel)
        .filter_by(username=request.username.lower())
        .first()
    )
    _ = get_translator(locale)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=_("user_not_found")
        )
    user_verify = user_obj.verify_password(request.password)
    if not user_verify:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_("invalid_password"),
        )

    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
    )
    _ = get_translator(locale)

    return {
        "message": _("login_success"),
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def user_logout(
    response: Response,
):
    response.delete_cookie(
        key="refresh_token", secure=True, httponly=True, samesite="strict"
    )


@router.post("/refresh")
async def user_refresh_token(request: UserRefreshTokenSchema):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(401, "No refresh token")
    user_id = decode_refresh_token(request.token)
    access_token = generate_access_token(user_id)
    return JSONResponse(
        content={
            "detail": "user token refresehd.",
            "access_token": access_token,
        }
    )


@router.get("/get-all")
async def get_all_users(db: Session = Depends(get_db)):
    all_users = db.query(UserModel.id, UserModel.username).all()
    user_list = [
        {"id": user.id, "username": user.username} for user in all_users
    ]
    return {"users": user_list}
