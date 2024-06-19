class APIKeyManager:
    def __init__(self):
        self.api_key_file = './API_KEYS.txt'
        self.api_keys = self.load_api_keys(self.api_key_file)

    def load_api_keys(self, api_key_file):
        with open(api_key_file, 'r') as file:
            return set([line.strip() for line in file.readlines()])

    def validate_api_key(self, api_key):
        return api_key in self.api_keys