from __future__ import annotations

import os
from pathlib import Path


def get_data_dir() -> Path:
    override = os.getenv("PAGETRAIL_HOME")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".pagetrail"

