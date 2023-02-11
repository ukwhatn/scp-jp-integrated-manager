import os
import random

import mmh3

from db.engine import Session
from db.models import UserApplicationPassword

CHAR_BORDER = "\u200B"
CHAR_ZERO = "\u200C"
CHAR_ONE = "\u200D"

HASH_BORDER = "\u2060"
HASH_ZERO = "\u2061"
HASH_ONE = "\u2062"


def _get_passwords() -> dict:
    """
    環境変数から合言葉を取得して辞書にする
    """
    passwords = {}
    cnt = 0
    while True:
        cnt += 1
        password = os.getenv("APPLICATION_PASSWORDS_" + str(cnt))
        if password is None:
            break
        passwords[cnt] = password
    return passwords


def encode_user_id(user_id: int) -> str:
    """
    ユーザIDを埋め込める状態にする
    """
    return str(bin(user_id)[2:]).replace("0", CHAR_ZERO).replace("1", CHAR_ONE)


def decode_user_id(password: str) -> int:
    """
    埋め込まれたユーザーIDを取得する
    """
    return int(password.split(CHAR_BORDER)[1].replace(CHAR_ZERO, "0").replace(CHAR_ONE, "1"), 2)


def decode_password(password: str) -> str:
    """
    埋め込みを削除して合言葉を取得する
    """
    return password.split(CHAR_BORDER)[0] + password.split(HASH_BORDER)[2]


def create_hash(password: str, user_id: int) -> int:
    """
    ユーザIDと合言葉をハッシュ化する
    """
    return mmh3.hash(password + str(user_id), os.getenv("APPLICATION_HASH_SEED"), signed=False)


def encode_hash(password_hash: int) -> str:
    """
    ハッシュを埋め込める状態にする
    """
    return str(bin(password_hash)[2:]).replace("0", HASH_ZERO).replace("1", HASH_ONE)


def decode_hash(password: str) -> int:
    """
    埋め込まれたハッシュを取得する
    """
    return int(password.split(HASH_BORDER)[1].replace(HASH_ZERO, "0").replace(HASH_ONE, "1"), 2)


def encode(password: str, user_id: int) -> str:
    """
    合言葉にキーを埋め込む
    """
    # ユーザIDを埋め込める状態にする
    encoded_user_id = encode_user_id(user_id)
    # 合言葉とユーザIDをまとめてハッシュ化する
    password_hash = create_hash(password, user_id)
    # ハッシュを埋め込める状態にする
    encoded_password_hash = encode_hash(password_hash)
    # 埋め込む位置をランダムに決める
    index = random.randint(1, len(password) - 2)
    # 埋め込み済合言葉を作成する
    return password[:index] + \
        CHAR_BORDER + encoded_user_id + CHAR_BORDER + \
        HASH_BORDER + encoded_password_hash + HASH_BORDER + \
        password[index:]


def is_valid_hash(password: str) -> bool:
    # ユーザIDを取得
    user_id = decode_user_id(password)
    # 合言葉を取得
    raw_password = decode_password(password)

    # ハッシュを取得
    raw_hash = decode_hash(password)

    # 取得した情報を再ハッシュ化したものと、埋め込まれたハッシュを比較する
    return raw_hash == create_hash(raw_password, user_id)


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
