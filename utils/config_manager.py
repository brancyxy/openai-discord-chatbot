import json
import os

from dotenv import load_dotenv

class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            load_dotenv()

            with open("config.json") as f:
                cls._instance._config = json.load(f)

        return cls._instance

    def get(self, key, default=None):
        if isinstance(key, str):
            env_val = os.getenv(key)
            if env_val is not None:
                return env_val

        # Handle nested keys
        keys = key.split(".") if isinstance(key, str) else key
        data = self._config

        try:
            for k in keys:
                data = data[k]
            return data
        except (KeyError, TypeError):
            return default