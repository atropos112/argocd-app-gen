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

#   1.2. Load config
with open(join(dirname(__file__), "config.yaml")) as f:
    config = yaml.safe_load(f)


# 2. Get all infrastructures
infras = []
for infra in config["infrastructures"]:
    infras.append(
        Infrastructure(
            context=InfrastructureContext(
                repo_path=Path(infra["repo_path"]),
                repo_url=infra["repo_url"],
                template=template,
            ),
            overrides= config.get("overrides", {}),
            infra_path=Path(infra["infra_path"]) if infra.get("infra_path") else None,
            )
    )

# 3. Clean up after previous call
generated_apps_path = Path(__file__).parent / "generated_apps"
if Path.is_dir(generated_apps_path):
    rmtree(generated_apps_path)
    print("Removed generated_apps directory.")

# 4. Generate yaml files from infrastructures and save them
for infra in infras:
    infra.save_to_files()
    print(f"Generated app yamls for:\n{infra}\n")
