import secrets
from datetime import datetime, timedelta

from db.engine import Session
from db.models import UserApplicationKey


def get_active_keys():
    with Session() as session:
        yesterday = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        keys = session.query(UserApplicationKey).filter(UserApplicationKey.created_at > yesterday).all()

    return [key.key for key in keys] if keys is not None and len(keys) > 0 else []


def create_key():
    with Session() as session:
        key = UserApplicationKey(
            key=secrets.token_urlsafe(15)
        )
        session.add(key)

    return key.key
