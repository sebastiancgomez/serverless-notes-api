from fastapi import Depends,FastAPI, HTTPException
from .service import (
    list_notes,
    get_note,
    create_new_note,
    delete_existing_note
)
from .models import NoteCreate,LoginRequest
from .auth import get_current_user, authenticate_user, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from .database import engine
from .db_models import Base
from .database import get_db
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user["username"],
        "role": user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
@app.get("/")
def root():
    return {"message": "API funcionando 🚀"}


@app.get("/notes")
def get_notes(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] == "admin":
        notes = list_notes(db)  # todas
    else:
        notes = list_notes(db, current_user["username"])

    return {
        "user": current_user["username"],
        "notes": notes
    }


@app.get("/notes/{note_id}")
def get_note_by_id(note_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    note = get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if note.owner != current_user["username"] and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    return note

@app.post("/notes")
def create_note_endpoint(note: NoteCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return {
        "user": current_user,
        "note": create_new_note(db, note.title, current_user["username"])
    }

@app.delete("/notes/{note_id}")
def delete_note_endpoint(
    note_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    delete_existing_note(db, note_id, current_user["username"], current_user["role"])

    return {
        "message": "Note deleted"
    }