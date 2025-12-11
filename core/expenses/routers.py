from typing import List
from fastapi import APIRouter, Depends
from users.models import UserModel
from expenses.models import *
from users.schemas import *
from sqlalchemy.orm import Session
from core.database import get_db
from auth.jwt_auth import *
from expenses.schemas import *
from i18n.translator import get_locale_lang, get_translator


router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/create", response_model=ExpenseResponseSchema)
async def create_expense(
    req_expense: BaseExpenseSchema,
    user: UserModel = Depends(get_auth_username),
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale_lang),
):
    new_expense = ExpenseModel(
        user_id=user.id,
        desc=req_expense.desc,
        amount=req_expense.amount,
    )
    _ = get_translator(locale)

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.get("/get-all", response_model=List[ExpenseResponseSchema])
async def get_all_expenses(
    db: Session = Depends(get_db), user: UserModel = Depends(get_auth_username)
):
    query = db.query(ExpenseModel).filter_by(user_id=user.id).all()
    return query


@router.get("/{item_id}", response_model=ExpenseResponseSchema)
async def get_expenses(
    item_id: int,
    db: Session = Depends(get_db),
):
    query = db.query(ExpenseModel).filter_by(id=item_id).first()
    return query


@router.delete("/delete/{expense_id}")
async def delete_expenses(
    expense_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_auth_username),
):
    expense = (
        db.query(ExpenseModel)
        .filter_by(id=expense_id, user_id=user.id)
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found.")

    db.delete(expense)
    db.commit()

    return {"message": f"Expense ID {expense_id} deleted successfully."}
