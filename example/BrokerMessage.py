from abc import ABC
from typing import Any


class BrokerMessage(ABC):

    @staticmethod
    def get(message: dict) -> Any:
        raise NotImplementedError

    @staticmethod
    def get_mandatory_fields() -> [str]:
        raise NotImplementedError

    @staticmethod
    def is_valid_message(message: dict) -> bool:
        raise NotImplementedError
