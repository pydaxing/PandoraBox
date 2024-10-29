import os
import secrets
import string
import uuid
from pathlib import Path

class APIKeyManager:
    def __init__(self):
        self._home_dir = Path.home()
        self._api_keys_file = self._home_dir / ".pbox" / "API_KEYS"

    def show_api_keys(self):
        with open(self._api_keys_file, 'r') as file:
            return set([line.strip() for line in file.readlines()])

    def _randomize_case(self, s):
        return ''.join(secrets.choice([c.lower(), c.upper()]) for c in s)

    def add_api_key(self):
        """Generates a new API key, adds it to the API_KEYS.txt file, updates the api_keys set, and returns the new key."""
        prefix = "pb-"
        random_length = 16  # 使用16个字符的随机字符串
        characters = string.ascii_letters + string.digits
        random_string1 = ''.join(secrets.choice(characters) for _ in range(random_length // 2))
        random_string2 = ''.join(secrets.choice(characters) for _ in range(random_length // 2))
        unique_id = uuid.uuid4().hex  # 生成一个唯一的UUID
        unique_id_random_case = self._randomize_case(unique_id)  # 随机大小写
        new_api_key = prefix + random_string1 + unique_id_random_case + random_string2

        with open(self._api_keys_file, 'a') as file:
            file.write(new_api_key + "\n")

        return new_api_key

    def del_api_key(self, api_key_to_remove):
        exists_api_keys = []
        with open(self._api_keys_file, 'r') as file:
            for api_key in file.readlines():
                exists_api_keys.append(api_key.strip())

        if api_key_to_remove in exists_api_keys:
            exists_api_keys.remove(api_key_to_remove)
            with open(self._api_keys_file, 'w') as file:
                file.write("\n".join(exists_api_keys))

    def check_api_key(self, api_key):
        api_keys = self.show_api_keys()
        return api_key in api_keys

