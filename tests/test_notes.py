import json
import pytest
from service.app.router import handle_request
from service.app.database import get_session, get_engine, Base


# 🔧 helper para crear eventos tipo API Gateway
def build_event(method, path, body=None, token=None):
    return {
        "httpMethod": method,
        "path": path,
        "headers": {
            "Authorization": f"Bearer {token}" if token else ""
        },
        "body": json.dumps(body) if body else None
    }


@pytest.fixture
def db():
    engine = get_engine()

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = get_session()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def auth_token(db):
    event = build_event(
        "POST",
        "/default/auth/login",
        body={"username": "sebastian", "password": "123456"}
    )

    response = handle_request(db, event)
    body = json.loads(response["body"])

    return body["access_token"]


# ✅ TEST: sin token
def test_get_notes_without_token(db):
    event = build_event("GET", "/default/notes")

    response = handle_request(db, event)

    assert response["statusCode"] == 401


# ✅ TEST: con token válido (sin datos)
def test_get_notes_empty(db, auth_token):
    event = build_event("GET", "/default/notes", token=auth_token)

    response = handle_request(db, event)
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert body["notes"] == []


# ✅ TEST: crear nota y luego obtenerla
def test_create_and_get_notes(db, auth_token):
    # Crear nota
    create_event = build_event(
        "POST",
        "/default/notes",
        body={"title": "Mi nota"},
        token=auth_token
    )

    create_response = handle_request(db, create_event)
    assert create_response["statusCode"] == 201

    # Obtener notas
    get_event = build_event("GET", "/default/notes", token=auth_token)
    get_response = handle_request(db, get_event)
    body = json.loads(get_response["body"])

    assert len(body["notes"]) >= 1
    assert body["notes"][0]["title"] == "Mi nota"


# ✅ TEST: usuario no ve notas de otro
def test_notes_isolation(db):
    # login user 1
    event1 = build_event(
        "POST",
        "/default/auth/login",
        body={"username": "sebastian", "password": "123456"}
    )
    token1 = json.loads(handle_request(db, event1)["body"])["access_token"]

    # login user 2
    event2 = build_event(
        "POST",
        "/default/auth/login",
        body={"username": "juan", "password": "123456"}
    )
    token2 = json.loads(handle_request(db, event2)["body"])["access_token"]

    # user1 crea nota
    create_event = build_event(
        "POST",
        "/default/notes",
        body={"title": "Nota privada"},
        token=token1
    )
    handle_request(db, create_event)

    # user2 consulta notas
    get_event = build_event("GET", "/default/notes", token=token2)
    response = handle_request(db, get_event)
    body = json.loads(response["body"])

    # user2 NO debería ver la nota
    assert all(note["title"] != "Nota privada" for note in body["notes"])


# ✅ TEST: delete (owner)
def test_delete_note_owner(db, auth_token):
    # crear
    create_event = build_event(
        "POST",
        "/default/notes",
        body={"title": "Eliminar"},
        token=auth_token
    )
    create_response = handle_request(db, create_event)
    note_id = json.loads(create_response["body"])["id"]

    # eliminar
    delete_event = build_event(
        "DELETE",
        f"/default/notes/{note_id}",
        token=auth_token
    )
    delete_response = handle_request(db, delete_event)

    assert delete_response["statusCode"] == 204