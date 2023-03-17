from dataclasses import dataclass


@dataclass
class RestConfig:
    host: str
    port: int
    protocol: str
