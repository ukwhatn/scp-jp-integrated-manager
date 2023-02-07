import os
import random

from db.engine import Session
from db.models import UserApplicationPassword

CHAR_BORDER = "\u200B"
CHAR_ZERO = "\u200C"
CHAR_ONE = "\u200D"


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


def encode(password: str, user_id: int) -> str:
    encoded_user_id = str(bin(user_id)[2:]).replace("0", CHAR_ZERO).replace("1", CHAR_ONE)
    index = random.randint(1, len(password) - 2)
    return password[:index] + CHAR_BORDER + encoded_user_id + CHAR_BORDER + password[index:]


def decode(password: str) -> int:
    return int(password.split(CHAR_BORDER)[1].replace(CHAR_ZERO, "0").replace(CHAR_ONE, "1"), 2)


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
                password=encode(passwords[index], user_id)
            )
            session.add(data)

    return data.password
