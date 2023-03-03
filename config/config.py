from pathlib import Path
import yaml
from config.singleton import *


@Singleton
class Config:
    def __init__(self, config_path: Path):
        self.data: dict = yaml.safe_load(config_path)
