from os import environ
from pathlib import Path


class InfrastructureContext:
    """
    This class is used to store the context of the infrastructure.
    """

    def __init__(
        self, repo_path: Path, repo_url: Path, template: dict, dev_mode: bool = None
    ):
        self.repo_path = repo_path
        self.repo_url = repo_url
        self.template = template
        if dev_mode is None:
            self.dev_mode = True if environ.get("ARGO_DEV_MODE", 0) == "1" else False
        else:
            self.dev_mode = dev_mode

    def __repr__(self):
        return f"Repo Path: {self.repo_path}\nRepo URL: {self.repo_url}\nDev Mode: {self.dev_mode}"

    def __str__(self):
        return self.__repr__()
