import secrets
import string
import uuid

def randomize_case(s):
    return ''.join(secrets.choice([c.lower(), c.upper()]) for c in s)

def generate_api_key():
    prefix = "pb-"
    random_length = 16  # 使用16个字符的随机字符串
    characters = string.ascii_letters + string.digits
    random_string1 = ''.join(secrets.choice(characters) for _ in range(random_length // 2))
    random_string2 = ''.join(secrets.choice(characters) for _ in range(random_length // 2))
    unique_id = uuid.uuid4().hex  # 生成一个唯一的UUID
    unique_id_random_case = randomize_case(unique_id)  # 随机大小写
    return prefix + random_string1 + unique_id_random_case + random_string2

api_key = generate_api_key()
print(api_key)