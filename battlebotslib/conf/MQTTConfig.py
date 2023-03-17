from dataclasses import dataclass


@dataclass
class MQTTConfig:
    destination_root: str
    username: str
    password: str
    host: str
    port: int
    connect_timeout: int
