from __future__ import annotations

import logging
from queue import SimpleQueue
from battlebotslib.utils.mqtt import MQTT
from battlebotslib.common.Messages import Messages
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from battlebotslib.ConnectionManager import ConnectionManager


class BotMqtt:

    @property
    def queue(self):
        return self._queue

    def __init__(self, connection_manager: ConnectionManager):
        self._connection_manager = connection_manager
        self._queue = SimpleQueue()
        MQTT().on_message(self._on_message)

    @staticmethod
    def start():
        """
        Start Mqtt client listening the topic.
        """
        MQTT().loop_start()

    @staticmethod
    def stop():
        """
        Start Mqtt client from listening the topic.
        """
        MQTT().loop_stop()

    def subscribe(self):
        """
        Subscribe to a topic and receive incoming messages.
        """
        MQTT().subscribe(self._connection_manager.bot_id)

    def _on_message(self, _client, _userdata, msg: MQTT.MQTTMessage):
        """
        Callback function on message received from MQTT.
        """
        # Transforming message to dict
        logging.debug("[MQTT] Incoming message")
        message = Messages.message_to_dict(msg.payload.decode('utf-8'), msg.topic)

        # Checking if the message is a connection id
        if 'msg_type' in message:
            if message['msg_type'] == 'mqtt_id':
                self._connection_manager.update_connection_ids(mqtt_id=message['data']['value'])
                return

        # Sending message to the internal queue
        self._queue.put(message)
