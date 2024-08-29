from enum import Enum

class ArtifactType(Enum):
    MAGIC_SCROLL = 1
    TREASURE = 2

class Artifact:
    def __init__(self, type):
        self.type = type