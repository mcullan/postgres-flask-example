from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String

# This creates a base we can inherit from
Base = declarative_base()

class Lost_Claimed(Base):
    __tablename__ = "lost_claimed"
    
    # sqlalchemy uses these names as the column names
    entry_time = Column(DateTime(timezone=True), primary_key=True)
    lost = Column(Integer)
    claimed = Column(Integer)
    
class Subcategory(Base):
    __tablename__ = 'subcategories'
    
    entry_time = Column(DateTime(timezone=True), primary_key=True)
    subcategory = Column(String, primary_key=True)
    category = Column(String, primary_key=True)
    count = Column(Integer)
    