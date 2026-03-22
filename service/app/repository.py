from typing import List, Optional
from sqlalchemy.orm import Session
from .db_models import NoteDB


def get_all_notes(db: Session, owner: str = None):
    query = db.query(NoteDB)
    if owner:
        query = query.filter(NoteDB.owner == owner)
    return query.all()


def get_note_by_id(db: Session, note_id: int):
    return db.query(NoteDB).filter(NoteDB.id == note_id).first()


def create_note(db: Session, title: str, owner: str):
    note = NoteDB(title=title, owner=owner)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, note: NoteDB):
    db.delete(note)
    db.commit()
    return True