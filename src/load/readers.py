import json
import yaml
from pathlib import Path
from typing import Any, Dict, List


def read_json(file_path: str | Path) -> Any:
    """
    Reads a JSON file and returns the parsed object.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist.")

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_channels_config(
    config_path: str = "config/channels.yml"
) -> List[Dict]:
    """
    Reads channels.yml.
    """

    file_path = Path(config_path)

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist.")

    with file_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)["channels"]


def get_channel_file_names(
    config_path: str = "config/channels.yml"
) -> List[str]:
    """
    Returns channel names formatted as filenames.

    Example:

    Ankit Bansal -> ankit_bansal
    """

    channels = load_channels_config(config_path)

    return [
        channel["name"].lower().replace(" ", "_")
        for channel in channels
    ]