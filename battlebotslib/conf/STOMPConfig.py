from dataclasses import dataclass


@dataclass
class STOMPConfig:
    destination_root: str
    username: str
    password: str
    host: str
    port: int
