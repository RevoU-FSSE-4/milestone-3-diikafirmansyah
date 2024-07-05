from models.base import Base
from sqlalchemy import Integer, ForeignKey, DateTime, DECIMAL, String


from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func


class Transaction(Base):
    __tablename__ = "transactions"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_account_id = mapped_column(Integer, ForeignKey("accounts.id"))
    to_account_id = mapped_column(Integer, ForeignKey("accounts.id"))
    amount = mapped_column(DECIMAL(10, 2))
    type = mapped_column(String(255))
    description = mapped_column(String(255))
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())