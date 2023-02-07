import secrets
from datetime import datetime, timedelta

from db.engine import Session
from db.models import UserApplicationKey


def get_active_keys(only_today: bool = False):
    with Session() as session:
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        if only_today:
            keys = session.query(UserApplicationKey).filter(UserApplicationKey.created_at > today).all()
        else:
            yesterday = today - timedelta(days=1)
            keys = session.query(UserApplicationKey).filter(UserApplicationKey.created_at > yesterday).all()

    return [key.key for key in keys] if keys is not None and len(keys) > 0 else []


def _create_key():
    with Session() as session:
        key = UserApplicationKey(
            key=secrets.token_urlsafe(15)
        )
        session.add(key)

    return key.key


def create_key_if_expired():
    if len(get_active_keys(only_today=True)) == 0:
        return _create_key()

    return None
