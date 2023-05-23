import src
from pathlib import Path


def get_path_repo() -> str:
    path_init = Path(src.__file__)
    path_repo = path_init.parent.parent.absolute()
    return str(path_repo)


def get_path_configs() -> str:
    path_repo = Path(get_path_repo())
    path_config = path_repo / "src" / "configs"
    return str(path_config)
