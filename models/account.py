from models.base import Base
from sqlalchemy import Integer, ForeignKey, DateTime, DECIMAL, VARCHAR


from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func


class Account(Base):
    __tablename__ = "accounts"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    account_type = mapped_column(VARCHAR(255), nullable=False)
    account_number = mapped_column(VARCHAR(255), unique=True)
    balance = mapped_column(DECIMAL(10, 2))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_at = mapped_column(DateTime(timezone=True), onupdate=func.now())

    # user = relationship("User", back_populates="accounts")
    # user = relationship("User", back_populates="accounts")
