from models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, DateTime, VARCHAR
from sqlalchemy.sql import func
import bcrypt


class User(Base):
    __tablename__= "users"

    id= mapped_column(Integer, primary_key=True, autoincrement=True)
    username= mapped_column(VARCHAR(255), nullable=True)
    email= mapped_column(VARCHAR(100), nullable=True)
    password_hash= mapped_column(VARCHAR(255), nullable=True)
    created_at= mapped_column(DateTime(timezone=True), server_default=func.now())
    update_at= mapped_column(DateTime(timezone=True), onupdate=func.now())

    def set_password(self, password_hash):
        self.password_hash = bcrypt.hashpw(
            password_hash.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password_hash):
        return bcrypt.checkpw(
            password_hash.encode("utf-8"), self.password_hash.encode("utf-8")
        )

    # accounts = relationship("Account", cascade="all, delete-orphan")
    # accounts = relationship("Account", back_populates="user")
