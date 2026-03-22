from .repository import (
    get_all_notes,
    get_note_by_id,
    create_note,
    delete_note
)
from sqlalchemy.orm import Session
from .exceptions import NotFoundError, ForbiddenError


def list_notes(db: Session, owner: str = None):
    if owner:
        return get_all_notes(db, owner)
    return get_all_notes(db)


def get_note(db: Session, note_id: int):
    note = get_note_by_id(db, note_id)
    if not note:
        raise NotFoundError("Note not found")
    return note


def create_new_note(db: Session, title: str, owner: str):
    return create_note(db, title, owner)


def delete_existing_note(db: Session, note_id: int, username: str, role: str):
    note = get_note_by_id(db, note_id)

    if not note:
        raise NotFoundError("Note not found")

    if note.owner != username and role != "admin":
        raise ForbiddenError("Forbidden")

    delete_note(db, note)