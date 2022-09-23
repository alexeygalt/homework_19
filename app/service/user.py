import base64
import hashlib
import hmac

from app.dao.user import UserDAO
from app.helpers.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def create(self, user_data):
        user_data['password'] = self.get_hash(user_data['password'])
        return self.dao.create(user_data)

    def update(self, user_data):
        user_data['password'] = self.get_hash(user_data['password'])
        return self.dao.update(user_data)

    def delete(self, uid):
        return self.dao.delete(uid)

    def get_hash(self, password) -> bytes:
        hash_password = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_password)

    def compare_passwords(self, password_hash, other_password) -> bool:
        decode_digest = base64.b64decode(password_hash)
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return hmac.compare_digest(decode_digest, hash_digest)
