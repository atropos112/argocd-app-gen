import sys
from copy import deepcopy
from os.path import abspath, dirname, join
from pathlib import Path, PurePath
from typing import List

# Add the parent directory to the Python path
parent_dir = abspath(join(dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

from apps.app import App
from infrastructure_context import InfrastructureContext


class HelmApp(App):
    def __init__(
        self,
        context: InfrastructureContext,
        values_file_path: Path,
        overrides: dict = {},
    ):
        self.value_file_path = values_file_path
        super().__init__(context, overrides)

    def get_name(self):
        return self.value_file_path.parts[-2]  # e.g. sonarr, radarr

    def get_scope(self):
        return self.value_file_path.name.split(".")[1]  # e.g. atro, trudo

    def get_namespace(self):
        return self.value_file_path.parts[-3]  # e.g. platform, media

    def get_app_rel_path(self):
        return self.value_file_path.parent.relative_to(self.context.repo_path).__str__()

    def setup_manifest(self) -> None:
        self.manifest["spec"]["source"]["helm"] = {}
        self.manifest["spec"]["source"]["helm"]["valueFiles"] = [self.value_file_path.name]
        super().setup_manifest()