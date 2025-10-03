from datetime import datetime
from fastapi import FastAPI, HTTPException, status, Depends
from schemas import BaseExpenseSchema, CreateExpenseSchema, BaseUserSchema, CreateUserSchema
from typing import List
from contextlib import asynccontextmanager
from database import Base, engine, get_db, User, Expense
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifspan(app: FastAPI):
    print("Application startup.")
    Base.metadata.create_all(engine)
    yield
    print("Application shutdown.")

app = FastAPI(lifespan=lifspan)

# ----------------------- User ----------------------------
@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=BaseUserSchema)
def create_user(req_user: CreateUserSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.name == req_user.name).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = User(
        name=req_user.name,
        email=req_user.email,
        password=req_user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users", response_model=list[BaseUserSchema])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all() 


@app.get("/user/{user_id}", response_model=BaseUserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.put('/user/{user_id}', status_code=status.HTTP_200_OK)
def update_info_user(user_id:int, req_user: CreateUserSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == user_id).one_or_none()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    existing_user.name = req_user.name
    existing_user.email = req_user.email
    existing_user.password = req_user.password
    db.commit()
    return {"message": f"Updated user-id: {existing_user.id}"}


@app.delete('/user/{req_user}', status_code=status.HTTP_200_OK)
def delete_content(req_user:int, db: Session =Depends(get_db)):
    user = db.query(User).filter(User.id == req_user).one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "Object removed successfully."},


# ----------------------- Expenses ----------------------------
@app.post('/user/{user_id}/expense', response_model=BaseExpenseSchema)
def create_expense(user_id: int, req_expense: CreateExpenseSchema, db: Session = Depends(get_db)): 
    new_expense = Expense(
        user_id=user_id,
        desc=req_expense.desc,
        amount=req_expense.amount,
        expense_date=req_expense.expense_date or datetime.now()
    ) 
    db.add(new_expense) 
    db.commit()
    db.refresh(new_expense)
    return new_expense


@app.get("/expenses", response_model=List[BaseExpenseSchema])
def get_all_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all() 


@app.get("/expense/{expense_id}", response_model=BaseExpenseSchema)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense


@app.put('/expense/{expense_id}', status_code=status.HTTP_200_OK)
def update_info_expense(expense_id:int, req_expense: CreateExpenseSchema, db: Session = Depends(get_db)):
    existing_expense = db.query(Expense).filter(Expense.id == expense_id).one_or_none()
    if not existing_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    
    existing_expense.desc = req_expense.desc
    existing_expense.amount = req_expense.amount
    db.commit()
    return {"message": f"Updated expense-id: {existing_expense.id}"}
