import os
import random

from db.engine import Session
from db.models import UserApplicationPassword

import mmh3

CHAR_BORDER = "\u200B"
CHAR_ZERO = "\u200C"
CHAR_ONE = "\u200D"

HASH_BORDER = "\u2060"
HASH_ZERO = "\u2061"
HASH_ONE = "\u2062"


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
    hashed_password = mmh3.hash(password+str(user_id), os.getenv("APPLICATION_HASH_SEED"), signed=False)
    encoded_hashed_password = str(bin(hashed_password)[2:]).replace("0", HASH_ZERO).replace("1", HASH_ONE)
    index = random.randint(1, len(password) - 2)
    return password[:index] + CHAR_BORDER + encoded_user_id + CHAR_BORDER + HASH_BORDER + encoded_hashed_password + HASH_BORDER + password[index:]


def decode(password: str) -> int:
    return int(password.split(CHAR_BORDER)[1].replace(CHAR_ZERO, "0").replace(CHAR_ONE, "1"), 2)

# def decode_hash(password: str) -> bool:
#     user_id = int(password.split(CHAR_BORDER)[1].replace(CHAR_ZERO, "0").replace(CHAR_ONE, "1"), 2)
#     raw_password = password.split(CHAR_BORDER)[0] + password.split(HASH_BORDER)[2]
#     raw_hash = int(password.split(HASH_BORDER)[1].replace(HASH_ZERO, "0").replace(HASH_ONE, "1"), 2)
#     hashed_password = mmh3.hash(raw_password+str(user_id), os.getenv("APPLICATION_HASH_SEED"), signed=False)
#     return raw_hash == hashed_password


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
