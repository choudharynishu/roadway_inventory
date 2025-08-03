from dataclasses import dataclass
from pathlib import Path

@dataclass
class config():
    size: int
    fov: int
    pitch: int
    api_key: str
    output_dir: Path