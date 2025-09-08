from db.engine import Session
from db.models import WikiAccessLog


def create(
        site_name: str,
        path: str,
        user_id: int,
        user_unix_name: str,
        ip_address: str,
        user_agent: str
):
    with Session() as session:
        access_log = WikiAccessLog(
            site_name=site_name,
            path=path,
            user_id=user_id,
            user_unix_name=user_unix_name,
            ip_address=ip_address,
            user_agent=user_agent
        )
        session.add(access_log)
