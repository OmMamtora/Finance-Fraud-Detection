from pathlib import Path
from typing import Any

import joblib
import yaml


def load_yaml(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def save_model(model: Any, path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)


def load_model(path: str) -> Any:
    return joblib.load(path)

