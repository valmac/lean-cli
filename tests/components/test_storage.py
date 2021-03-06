import json
from pathlib import Path

from lean.components.storage import Storage


def test_get_reads_key_from_file() -> None:
    path = Path.cwd() / "config.json"
    with path.open("w+") as file:
        file.write('{ "key": "value" }')

    storage = Storage(str(path))

    assert storage.get("key") == "value"


def test_get_returns_default_when_key_not_set() -> None:
    path = Path.cwd() / "config.json"
    with path.open("w+") as file:
        file.write('{ "key": "value" }')

    storage = Storage(str(path))

    assert storage.get("key2", "my-default") == "my-default"


def test_set_overrides_values_in_existing_file() -> None:
    path = Path.cwd() / "config.json"
    with path.open("w+") as file:
        file.write('{ "key": "value" }')

    storage = Storage(str(path))
    storage.set("key", "new-value")

    data = json.loads(path.read_text())
    assert data == {"key": "new-value"}


def test_set_creates_new_file_when_file_does_not_exist() -> None:
    path = Path.cwd() / "config.json"

    storage = Storage(str(path))
    storage.set("key", "value")

    data = json.loads(path.read_text())
    assert data == {"key": "value"}


def test_has_returns_true_when_key_exists_in_file() -> None:
    path = Path.cwd() / "config.json"
    with path.open("w+") as file:
        file.write('{ "key": "value" }')

    storage = Storage(str(path))

    assert storage.has("key")


def test_has_returns_false_when_key_does_not_exist_in_file() -> None:
    path = Path.cwd() / "config.json"
    with path.open("w+") as file:
        file.write('{ "key": "value" }')

    storage = Storage(str(path))

    assert not storage.has("key2")


def test_has_returns_false_when_file_does_not_exist() -> None:
    path = Path.cwd() / "config.json"

    storage = Storage(str(path))

    assert not storage.has("key")


def test_clear_deletes_file() -> None:
    path = Path.cwd() / "config.json"
    with path.open("w+") as file:
        file.write('{ "key": "value" }')

    storage = Storage(str(path))
    storage.clear()

    assert not path.exists()
