import os 
import json
from pathlib import Path

from dataclasses import dataclass

@dataclass
class Config:
    config_dir: Path
    filenames: list[str]

    def _read_file(self, filename: str):
        with self.config_dir.joinpath(filename).open("r") as f:
           yield json.load(f)
    
    def load(self) -> dict[str, str]:
        for file in self.filenames:
            yield from self._read_file(file)

    