import os
import secrets
import string
import uuid

class APIKeyManager:
    def __init__(self):
        self.api_key_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'API_KEYS.txt'))
        self.api_keys = self.load_api_keys()

    def load_api_keys(self):
        with open(self.api_key_file, 'r') as file:
            return set([line.strip() for line in file.readlines()])

    def validate_api_key(self, api_key):
        return api_key in self.api_keys

    def _randomize_case(self, s):
        return ''.join(secrets.choice([c.lower(), c.upper()]) for c in s)
    def generate_api_key(self):
        """Generates a new API key, adds it to the API_KEYS.txt file, updates the api_keys set, and returns the new key."""
        prefix = "pb-"
        random_length = 16  # 使用16个字符的随机字符串
        characters = string.ascii_letters + string.digits
        random_string1 = ''.join(secrets.choice(characters) for _ in range(random_length // 2))
        random_string2 = ''.join(secrets.choice(characters) for _ in range(random_length // 2))
        unique_id = uuid.uuid4().hex  # 生成一个唯一的UUID
        unique_id_random_case = self._randomize_case(unique_id)  # 随机大小写
        new_api_key = prefix + random_string1 + unique_id_random_case + random_string2

        # 将新的 API 密钥写入文件并更新 api_keys 集合
        with open(self.api_key_file, 'a') as file:
            file.write(new_api_key + '\n')
        self.api_keys.add(new_api_key)  # Update the api_keys set with the new key

        return new_api_key