from pathlib import Path

project_src_directory = Path(__file__).parent
project_directory = project_src_directory.parent
project_data_directory = project_directory / "data"

__all__ = (
    "project_src_directory",
    "project_directory",
    "project_data_directory",
)
