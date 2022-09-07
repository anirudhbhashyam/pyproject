from pathlib import Path
from dataclasses import dataclass, field

from config import Config

@dataclass
class Project:
    name: str
    path: Path
    project_dir: Path = field(
        init = False
    )
    working_dir: Path = field(
        init = False
    )
    dirs: dict[str, str] = field(
        init = False
    )
    files: dict[str, str] = field(
        init = False
    )
    templates: dict[str, str] = field(
        init = False
    )
    _config_data: dict[str, str] = field(
        init = False
    )

    def __post_init__(self) -> None:
        config = Config(
            config_dir = Path(__file__).parents[1].joinpath("config"),
            filenames = ["settings.json"]
        )
        self._config_data = next(config.load())
        self.project_dir = self.path.joinpath(self.name)
        self.working_dir = Path(__file__).parents[1]

        self.dirs = self._config_data["PROJECT_DIRS"]
        self.files = self._config_data["PROJECT_FILES"]
        self.templates = self._config_data["PROJECT_TEMPLATES"]

    def create_project(self) -> None:
        self.project_dir.mkdir(parents = True, exist_ok = True)
        self._create_dirs()
        self._create_files()
        
        for template in self.templates:
            self._write_project_template(template)

    def _create_dirs(self) -> None:
        for _, dir_path in self.dirs.items():
            dir_to_create = self.project_dir.joinpath(dir_path).resolve()
            dir_to_create.mkdir(parents = True, exist_ok = True)

    def _create_files(self) -> None:
        for _, file_path in self.files.items():
            file_to_create = self.project_dir.joinpath(file_path).resolve()
            file_to_create.touch(exist_ok = True)

    def _write_project_template(self, template: str) -> None:
        template = template.upper()

        if template not in self.templates or template not in self.files:
            raise KeyError(f"Requested {template = } does not exist. Check the settings.json or the templates directory.")

        template_file = self.working_dir.joinpath(self.templates[template])
        write_file = self.project_dir.joinpath(self.files[template])

        if not write_file.exists():
            raise FileNotFoundError(f"{template.lower()}.txt file does not exist.")
        
        with open(template_file, "r") as f:
            to_write = f.read()

        with open(write_file, "w") as f:
            f.write(to_write)