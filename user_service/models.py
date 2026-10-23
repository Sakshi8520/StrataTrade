from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class User(Base):
	__tablename__ = "users"
	id : Mapped[int] = mapped_column(primary_key=True)
	username : Mapped[str]  = mapped_column(String,unique=True,nullable=False)
	email : Mapped[str] = mapped_column(String,unique=True,nullable=False)
	password_hash : Mapped[str] = mapped_column(String,nullable=False)
