import json
import logging
from service.app.database import  get_session, get_engine
from service.app.db_models import Base
from service.app.router import handle_request
from service.app.exceptions import NotFoundError, ForbiddenError




logger = logging.getLogger()
logger.setLevel(logging.INFO)

Base.metadata.create_all(bind=get_engine())

def lambda_handler(event, context):
    db = get_session()

    try:
        logger.info(f"EVENT: {json.dumps(event)}")
        return handle_request(db, event)

        

    except NotFoundError as e:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": str(e)})
        }

    except ForbiddenError as e:
        return {
            "statusCode": 403,
            "body": json.dumps({"error": str(e)})
        }

    except Exception as e:
        logger.error(str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"})
        }

    finally:
        db.close()