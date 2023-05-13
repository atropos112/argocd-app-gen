# 1. Preparation
#   1.1. Load template
#   1.2. Load ignore differences
# 2. Get all infrastructures
# 3. Clean up after previous call
# 4. Generate yaml files from infrastructures and save them


from os import environ
from os.path import dirname, isdir, join, realpath
from pathlib import Path
from shutil import rmtree
import yaml

from infrastructure import Infrastructure
from infrastructure_context import InfrastructureContext

# 1. Preparation
#   1.1. Load template
with open(join(dirname(__file__), "app.tpl")) as f:
    template = yaml.safe_load(f)

#   1.2. Load overrides
with open(join(dirname(__file__), "overrides.yaml")) as f:
    overrides = yaml.safe_load(f)


# 2. Get all infrastructures
infras = [
    Infrastructure(
        context=InfrastructureContext(
            repo_path=Path("/home/atropos/projects/Infra/k3s"),
            repo_url="git@gitlab.atro.xyz:inf/charts.git",
            template=template,
        ),
        overrides=overrides,
        infra_path=Path("/home/atropos/projects/Infra/k3s/apps"),
    ),
    Infrastructure(
        context=InfrastructureContext(
            repo_path=Path("/home/atropos/projects/Infra/k3s"),
            repo_url="git@github.com:atropos112/k3s.git",
            template=template,
        ),
        overrides=overrides,
        infra_path=Path("/home/atropos/projects/Infra/k3s/core"),
    ),
    Infrastructure(
        context=InfrastructureContext(
            repo_path=Path("/home/atropos/projects/Infra/pipelines"),
            repo_url="git@gitlab.atro.xyz:inf/pipelines.git",
            template=template,
        ),
        overrides=overrides
    ),
]

# 3. Clean up after previous call
generated_apps_path = Path(__file__).parent / "generated_apps"
if Path.is_dir(generated_apps_path):
    rmtree(generated_apps_path)
    print("Removed generated_apps directory.")

# 4. Generate yaml files from infrastructures and save them
for infra in infras:
    infra.save_to_files()
    print(f"Generated app yamls for:\n{infra}\n")
