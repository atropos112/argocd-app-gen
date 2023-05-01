# Infrastructure class, which is used to represent the infrastructure folder structure.

# The Infrastructure class will have the following:
# - Get all apps from the infrastructure folder. This will be done by the get_apps() method.
# - Save all apps to files. This will be done by the save_apps_to_files() method.


from os import listdir, remove
from os.path import dirname, isdir, join
from pathlib import Path
from shutil import rmtree
from typing import Dict, List

import yaml

from apps.app import App
from apps.appshelper import create_apps_from_path
from ignore_difference import IgnoreDifference
from infrastructure_context import InfrastructureContext
from kind import Kind


class Infrastructure:
    """
    This class is used to represent the infrastructure folder structure.
    If the infra_path is not provided it is assumend the repo_path is the infra path.
    The purpose of this class is to get all apps from the infrastructure folder and save them to files.
    """

    def __init__(
        self,
        context: InfrastructureContext,
        infra_path: Path = None,
        ignore_differences: Dict[str, IgnoreDifference] = {},
    ) -> None:
        self.context = context
        self.infra_path = self.context.repo_path if infra_path is None else infra_path
        self.ignore_differences = ignore_differences

        self.apps = self.get_apps()

    def __repr__(self):
        return (
            f"{self.context}\nInfrastructure Path: {self.infra_path}\nApps: {self.apps}"
        )

    def __str__(self):
        return (
            f"{self.context}\nInfrastructure Path: {self.infra_path}\nApps: {self.apps}"
        )

    def get_apps(self) -> List[App]:
        # The structure of the infrastructure folder is as follows:
        # infra_path:
        # - non-scoped namespaces
        #   - app folders
        #     - app files (including values overides if its a helm chart)

        apps = []
        for non_scoped_namespace in (
            ns
            for ns in Path.iterdir(self.infra_path)
            if ns.is_dir() and not ns.name.startswith(".")
        ):
            for app_folder in (
                f
                for f in Path.iterdir(non_scoped_namespace)
                if f.is_dir() and not f.name.startswith(".")
            ):
                apps.extend(
                    create_apps_from_path(
                        self.context,
                        app_folder,
                        self.ignore_differences.get(app_folder.name, None),
                    )
                )

        return apps

    def save_to_files(self) -> None:
        for app in self.apps:
            app.save_to_file()
