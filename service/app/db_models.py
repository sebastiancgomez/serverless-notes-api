from sqlalchemy import Column, Integer, String
from .database import Base

class NoteDB(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    owner = Column(String, index=True)