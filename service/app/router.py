from .service import create_new_note, delete_existing_note, get_note, list_notes
from .exceptions import NotFoundError, ForbiddenError
import json
from .auth import  authenticate_user, create_access_token, get_current_user_from_token


def handle_request(db, event):
    http_method = event.get("httpMethod")
    path = event.get("path")
    print("PATH:", path)
    print("METHOD:", http_method)
    normalized_path = path.split("/default")[-1]
    
    # 🔐 LOGIN
    if http_method == "POST" and normalized_path == "/auth/login":
        body = event.get("body")

        if not body:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing body"})
            }

        data = json.loads(body)

        username = data.get("username")
        password = data.get("password")
        

        if not username or not password:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "Username and password required"})
            }

        user = authenticate_user(username, password)
        
        if not user:
             return {
                "statusCode": 401,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "Invalid credentials"})
            }

        token = create_access_token({
            "sub": user["username"],
            "role": user["role"]
        })

        return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"access_token": token, "token_type": "bearer"})
          }
    # 📄 GET NOTE BY ID
    if http_method == "GET" and normalized_path.startswith("/notes/"):
        try:
            note_id = int(normalized_path.split("/notes/")[-1])
        except ValueError:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid note id"})
            }

        token = get_token_from_event(event)

        if not token:
            return {
                "statusCode": 401,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "Missing token"})
            }

        try:
            user = get_current_user_from_token(token)
        except Exception:
            return {
                "statusCode": 401,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "Invalid token"})
            }

        note = get_note(db, int(note_id))

        if not note:
            return {
                "statusCode": 404,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "Note not found"})
            }

        # 🔐 seguridad
        if note.owner != user["username"] and user["role"] != "admin":
            return {
                "statusCode": 403,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "Forbidden"})
            }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(serialize_note(note))
        }
    # 📄 GET NOTES
    if http_method == "GET" and normalized_path == "/notes":

        token = get_token_from_event(event)

        if not token:
            return {
                "statusCode": 401,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "Missing token"})
            }

        try:
            print("TOKEN:", token)
            user = get_current_user_from_token(token)
        except Exception:
            return {
                "statusCode": 401,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "Invalid token"})
            }

        notes = list_notes(db, user["username"])
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "notes": [serialize_note(n) for n in (notes or [])]
            })
        }
        return response
    # ✏️ CREATE NOTE
    if http_method == "POST" and normalized_path == "/notes":

        token = get_token_from_event(event)

        if not token:
            return {
                "statusCode": 401,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "Missing token"})
            }

        try:
            user = get_current_user_from_token(token)
        except Exception:
            return {
                "statusCode": 401,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "Invalid token"})
            }

        body = event.get("body")

        if not body:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "Missing body"})
            }

        data = json.loads(body)
        title = data.get("title")

        if not title:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "Title is required"})
            }

        note = create_new_note(db, title, user["username"])

        return {
            "statusCode": 201,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(serialize_note(note))
        }
        
    # 🗑️ DELETE NOTE
    if http_method == "DELETE" and normalized_path.startswith("/notes/"):
        try:
            note_id = int(normalized_path.split("/notes/")[-1])
        except ValueError:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid note id"})
            }
            
        token = get_token_from_event(event)

        if not token:
            return {
                "statusCode": 401,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "Missing token"})
            }

        try:
            user = get_current_user_from_token(token)
        except Exception:
            return {
                "statusCode": 401,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "Invalid token"})
            }

        note = get_note(db, int(note_id))

        if not note:
            return {
                "statusCode": 404,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "Note not found"})
            }

        # 🔐 seguridad
        if note.owner != user["username"] and user["role"] != "admin":
            return {
                "statusCode": 403,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "Forbidden"})
            }

        delete_existing_note(db, note.id, user["username"], user["role"])

        return {
            "statusCode": 204,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": ""
        }    

    return {
        "statusCode": 404,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({"message": "Not found"})
    }

def get_token_from_event(event):
    headers = event.get("headers") or {}

    auth_header = headers.get("Authorization") or headers.get("authorization")

    if not auth_header:
        return None

    if not auth_header.startswith("Bearer "):
        return None

    return auth_header.split(" ")[1]

def serialize_note(note):
    if not note:
        return None
    return {
        "id": note.id,
        "title": note.title,
        "owner": note.owner
    }