from fastapi import FastAPI
from models import Expense
from datetime import datetime
import uuid

app = FastAPI()
from database import engine, SessionLocal

# import schemas
import schemas as schemas
from fastapi.params import Depends
from sqlalchemy.orm import Session


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


@app.get("/expenses", status_code=200)
async def get_expenses(db: Session = Depends(get_db)):
    expenses = db.query(schemas.Expense).all()
    return expenses
