from __future__ import annotations

import logging
from typing import Any, Generator
from BrokerMessage import BrokerMessage


class DetectedObject(BrokerMessage):

    @property
    def angle_from(self) -> float:
        return self._from

    @property
    def angle_to(self) -> float:
        return self._to

    @property
    def object_type(self) -> str:
        return self._object_type

    @property
    def name(self) -> str:
        return self._name

    @property
    def distance(self) -> float:
        return self._distance

    def __init__(self, message_data: dict):
        self._from = message_data['from']
        self._to = message_data['to']
        self._object_type = message_data['object_type']
        self._name = message_data['name']
        self._distance = message_data['distance']

    @staticmethod
    def get(message: dict) -> Generator[DetectedObject, Any, Any]:
        if len(message.keys()) > 0:
            if DetectedObject.is_valid_message(message):
                for detected_object in message['data']:
                    yield DetectedObject(detected_object)
            else:
                logging.error(f"Message de détection d'objet malformé : \n{message}")
                return list()
        return list()

    @staticmethod
    def get_mandatory_fields() -> list[str]:
        return ['msg_type', 'source', 'data']

    @staticmethod
    def is_valid_message(message: dict) -> bool:
        for field in DetectedObject.get_mandatory_fields():
            if field not in message:
                return False
        return True
