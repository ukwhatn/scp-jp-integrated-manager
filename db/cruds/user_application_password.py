import os
import random

from db.engine import Session
from db.models import UserApplicationPassword


def _get_passwords() -> dict:
    passwords = {}
    cnt = 0
    while True:
        cnt += 1
        password = os.getenv("APPLICATION_PASSWORDS_" + str(cnt))
        if password is None:
            break
        passwords[cnt] = password
    return passwords


def get(user_id: int):
    with Session() as session:
        # DBから合言葉を取得する
        data = session.query(UserApplicationPassword).filter(UserApplicationPassword.user_id == user_id).first()

        if data is None:
            # 合言葉をenvから取得
            passwords = _get_passwords()

            # randomを作成
            index = random.randint(min(passwords.keys()), max(passwords.keys()))

            # DBに合言葉を登録
            data = UserApplicationPassword(
                user_id=user_id,
                password=passwords[index]
            )
            session.add(data)

    return data.password
