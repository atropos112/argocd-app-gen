import sys
from copy import deepcopy
from os import listdir, remove
from os.path import abspath, dirname, isdir, join
from pathlib import Path
from shutil import rmtree
from typing import List

import yaml

# Add the parent directory to the Python path
parent_dir = abspath(join(dirname(__file__), ".."))
sys.path.insert(0, parent_dir)
from apps.app import App
from apps.helmapp import HelmApp
from apps.yamlapp import YamlApp
from ignore_difference import IgnoreDifference
from infrastructure_context import InfrastructureContext

# We create an App, which is a HelmApp or a YamlApp.
# The App class is the parent class of both HelmApp and YamlApp.
# In each case the scope is to be determined by either the name of the folder (if yaml) or by the name of the values file (if helm).


def create_apps_from_path(
    context: InfrastructureContext,
    app_path: Path,
    ignore_differences: List[IgnoreDifference],
) -> List[App]:
    apps = []

    match len(list(app_path.glob("Chart.y*ml"))):
        case 0:
            apps.append(YamlApp(context, app_path, ignore_differences))
        case 1:
            for value_file_path in (file for file in app_path.glob("values.*.y*ml")):
                apps.append(HelmApp(context, value_file_path, ignore_differences))
        case _:
            raise Exception(
                "There are more than one Chart.y*ml files in the app folder."
            )

    return apps
