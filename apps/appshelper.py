import sys
from copy import deepcopy
from os import listdir, remove
from os.path import abspath, dirname, isdir, join
from pathlib import Path
from shutil import rmtree
from typing import List

import yaml

from apps.atroapp import AtroApp

# Add the parent directory to the Python path
parent_dir = abspath(join(dirname(__file__), ".."))
sys.path.insert(0, parent_dir)
from apps.app import App
from apps.helmapp import HelmApp
from apps.yamlapp import YamlApp
from infrastructure_context import InfrastructureContext

# We create an App, which is a HelmApp or a YamlApp.
# The App class is the parent class of both HelmApp and YamlApp.
# In each case the scope is to be determined by either the name of the folder (if yaml) or by the name of the values file (if helm).


def create_apps_from_path(
    context: InfrastructureContext,
    app_path: Path,
    overrides: dict,
) -> List[App]:
    apps = []

    if len(list(app_path.glob("Chart.y*ml"))) == 1:
        for value_file_path in (file for file in app_path.glob("values.*.y*ml")):
            apps.append(HelmApp(context, value_file_path, overrides))
    elif len(list(app_path.glob("Atro.yaml"))) == 1:
        for value_file_path in (file for file in app_path.glob("values.*.y*ml")):
            apps.append(AtroApp(context, value_file_path, overrides))
    else:
        apps.append(YamlApp(context, app_path, overrides))

    return apps
