from sqlalchemy import Column, Integer, String
from database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=False)
    url = Column(String, nullable=True)


"""

# Define the User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    account_status = Column(String, nullable=False)
    subscription_plan = Column(String, nullable=False)
"""
