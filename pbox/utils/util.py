from .secret import APIKeyManager

api_key_manager = APIKeyManager()

def new_api_key():
    api_key = api_key_manager.generate_api_key()
    print(api_key)
    return api_key

def look_api_key():
    api_keys = api_key_manager.load_api_keys()
    print('\n'.join(api_keys))
    return api_keys
