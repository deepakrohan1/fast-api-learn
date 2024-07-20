from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
import schemas as schemas
from database import engine, SessionLocal
import models as models
from models import Expense
from datetime import datetime
import uuid

app = FastAPI()

# import schemas


expenses = [
    Expense(
        expense_id=str(uuid.uuid4()),
        title="Rent",
        description="Rent of house",
        amount=1000,
        category="Housing",
        spent_on=datetime(2022, 1, 1),
    ),
    Expense(
        expense_id=str(uuid.uuid4()),
        title="Groceries",
        description="Groceries of month",
        amount=200,
        category="Food",
        spent_on=datetime(2022, 1, 2),
    ),
    Expense(
        expense_id=str(uuid.uuid4()),
        title="Utilities",
        amount=300,
        description="intenet and ph bills",
        category="Bills",
        spent_on=datetime(2022, 1, 3),
    ),
]

schemas.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/expenses", status_code=201)
async def create_expense(expense: Expense, db: Session = Depends(get_db)):
    new_product = schemas.Expense(**expense.dict())
    db.add(new_product)
    db.commit()

"""
Get only certain fields to be displayed using response_model
"""
@app.get("/expenses", status_code=200, response_model=list[models.ExpenseResponse])
async def get_expenses(db: Session = Depends(get_db)):
    expenses = db.query(schemas.Expense).all()
    return expenses

@app.get("/expenses/{expense_id}", status_code=200)
async def get_expense(expense_id: str, db: Session = Depends(get_db)):
    expense = db.query(schemas.Expense).filter(schemas.Expense.expense_id == expense_id).first()
    return expense

@app.put("/expenses/{expense_id}", status_code=200)
async def update_expense(expense_id: str, expense: Expense, db: Session = Depends(get_db)):
    expense_db = db.query(schemas.Expense).filter(schemas.Expense.expense_id == expense_id).first()

    if expense_db:
        expense_db.title = expense.title
        expense_db.description = expense.description
        expense_db.amount = expense.amount

    db.commit()
    return {"message": "Expense updated successfully"}

# Dont show all data in a model
"""
Defining the respone model
"""