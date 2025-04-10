from dataclasses import dataclass

@dataclass 
class ProjectInfo:
    """Class for maintaining project info like vulnerablilities and image size"""
    low: int = 0
    medium: int = 0
    high: int = 0
    critical: int = 0
    size: int = 0

    @property
    def size_mb(self) -> float:
        return self.size/1000000
