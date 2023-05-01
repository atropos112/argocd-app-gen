import os
import sys
from copy import deepcopy
from pathlib import Path
from typing import List

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

# Now you should be able to import IgnoreDifference from ignore_difference module
from apps.app import App
from ignore_difference import IgnoreDifference
from infrastructure_context import InfrastructureContext


class YamlApp(App):
    def __init__(
        self,
        context: InfrastructureContext,
        app_path: Path,
        ignore_differences: List[IgnoreDifference] = [],
    ):
        self.app_path = app_path
        super().__init__(context, ignore_differences)

    def get_name(self) -> str:
        return self.app_path.name  # e.g. sonarr, radarr

    def get_scope(self) -> str:
        scope_overides = list(self.app_path.glob("scope.*"))

        match len(scope_overides):
            case 0:
                return "atro"
            case 1:
                return scope_overides[0].name.split(".")[1]  # e.g. atro, trudo
            case _:
                raise ValueError("Multiple scope overrides found.")

    def get_namespace(self) -> str:
        return self.app_path.parts[-2]  # e.g. platform, media

    def get_app_rel_path(self):
        return self.app_path.relative_to(self.context.repo_path).__str__()

    def setup_manifest(self) -> None:
        super().setup_manifest()
        self.manifest["spec"]["source"]["directory"] = {}
        self.manifest["spec"]["source"]["directory"]["jsonnet"] = {}
        self.manifest["spec"]["source"]["directory"]["recurse"] = True