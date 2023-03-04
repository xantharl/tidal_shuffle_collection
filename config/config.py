from pathlib import Path
import yaml
from config.singleton import *


@Singleton
class Config:
    def __init__(self, config_path: Path = Path("config/config.yml")):
        with open(config_path, "r") as config:
            self.data: dict = yaml.safe_load(config)
