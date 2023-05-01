import sys
from abc import ABC, abstractmethod
from copy import deepcopy
from os import listdir, makedirs
from os.path import abspath, dirname, exists, isdir, isfile, join, relpath
from typing import List
from pathlib import Path
import yaml

parent_dir = abspath(join(dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

from ignore_difference import IgnoreDifference
from infrastructure_context import InfrastructureContext


class App(ABC):
    def __init__(
        self, context: InfrastructureContext, ignore_differences: List[IgnoreDifference]
    ) -> None:
        self.context = context
        self.ignore_differences = ignore_differences

        self.manifest = deepcopy(context.template)
        self.scope = self.get_scope()
        self.name = self.get_name()
        self.namespace = self.get_namespace()
        self.app_rel_path = self.get_app_rel_path()

        self.setup_manifest()

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.namespace}/{self.name}/{self.scope}"

    @abstractmethod
    def get_name(self) -> str:
        raise ReferenceError(
            "Shouldn't be called, from abstract class, only from its child classes"
        )

    @abstractmethod
    def get_scope(self) -> str:
        raise ReferenceError(
            "Shouldn't be called, from abstract class, only from its child classes"
        )

    @abstractmethod
    def get_namespace(self) -> str:
        raise ReferenceError(
            "Shouldn't be called, from abstract class, only from its child classes"
        )

    @abstractmethod
    def get_app_rel_path(self) -> str:
        raise ReferenceError(
            "Shouldn't be called, from abstract class, only from its child classes"
        )

    def save_to_file(self) -> None:
        # Dump manifest into yaml, generate necessary folders and save it to correct file
        app_yaml = yaml.dump(self.manifest)
        output_dir = Path(__file__).parent.parent / "generated_apps" / self.namespace / self.name
        output_dir.mkdir(parents=True, exist_ok=True)  # Create directories if they don't exist
        open(output_dir / f"{self.scope}.yaml", "w+").write(app_yaml)

    @abstractmethod
    def setup_manifest(self) -> None:
        # App name + scope if not default scope e.g. sonarr-yi, authelia-trudo, radarr
        self.manifest["metadata"]["name"] = (
            self.name if self.scope == "atro" else f"{self.name}-{self.scope}"
        )

        # Namespace e.g. platform-trudo, platform, media-yi
        self.manifest["spec"]["destination"]["namespace"] = (
            self.namespace if self.scope == "atro" else f"{self.namespace}-{self.scope}"
        )

        # App path
        self.manifest["spec"]["source"]["path"] = self.app_rel_path
        self.manifest["metadata"]["annotations"]["argocd.argoproj.io/manifest-generate-paths"] = "/" + self.app_rel_path

        # Repo URL
        self.manifest["spec"]["source"]["repoURL"] = self.context.repo_url

        # Sync policies
        self.manifest["spec"]["syncPolicy"] = {}
        self.manifest["spec"]["syncPolicy"]["syncOptions"] = [
            "RespectIgnoreDifferences=true"
        ]
        if self.context.dev_mode:
            self.manifest["spec"]["syncPolicy"]["automated"] = None
        else:
            self.manifest["spec"]["syncPolicy"]["automated"] = {}
            self.manifest["spec"]["syncPolicy"]["automated"]["prune"] = True
            self.manifest["spec"]["syncPolicy"]["automated"]["selfHeal"] = True

        # Ignore differences
        if self.ignore_differences:
            self.manifest["spec"]["ignoreDifferences"] = [ignore_dif.to_json() for ignore_dif in self.ignore_differences]