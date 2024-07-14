from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Expense(Base):
    __tablename__ = "expenses"
    expense_id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    title = Column(String(100))
    description = Column(String(500))
    amount = Column(Integer)
    category = Column(String(100))
    spent_on = Column(DateTime)
