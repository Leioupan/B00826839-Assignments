"""Singleton exercise: load application configuration only once per process."""
from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import Any


class ConfigManager:
    _instance: ConfigManager | None = None
    _instance_lock = Lock()

    def __new__(cls, path: str | Path = "config.json") -> ConfigManager:
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, path: str | Path = "config.json") -> None:
        if self._initialized:
            return
        self.path = Path(path)
        with self.path.open(encoding="utf-8") as config_file:
            self._config: dict[str, Any] = json.load(config_file)
        self._initialized = True

    @classmethod
    def get_instance(cls, path: str | Path = "config.json") -> ConfigManager:
        return cls(path)

    def get(self, key: str, default: Any = None) -> Any:
        value: Any = self._config
        for part in key.split("."):
            if not isinstance(value, dict) or part not in value:
                return default
            value = value[part]
        return value


if __name__ == "__main__":
    manager = ConfigManager.get_instance()
    print("App:", manager.get("app.name"))
    print("Database host:", manager.get("database.host"))
