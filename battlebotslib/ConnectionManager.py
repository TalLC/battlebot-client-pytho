from __future__ import annotations

import logging
from battlebotslib.utils.rest import Rest
from battlebotslib.utils.BotMqtt import BotMqtt
from battlebotslib.utils.BotStomp import BotStomp
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from queue import SimpleQueue


class ConnectionManager:

    @property
    def bot_id(self) -> str:
        return self._bot_id

    @property
    def is_bot_registered(self) -> bool:
        return self._is_bot_registered

    @property
    def is_connection_requested(self) -> bool:
        return self._is_connection_requested

    @property
    def are_all_services_connected(self) -> bool:
        return self._all_services_connected

    @property
    def mqtt_queue(self) -> SimpleQueue:
        return self._bot_mqtt.queue

    @property
    def stomp_queue(self) -> SimpleQueue:
        return self._bot_stomp.queue

    def __init__(self):
        self._bot_id = str()
        self._rest_id = str()
        self._stomp_id = str()
        self._mqtt_id = str()

        self._is_bot_registered = False
        self._is_connection_requested = False
        self._all_services_connected = False

        self._bot_mqtt = BotMqtt(self)
        self._bot_stomp = BotStomp(self)

    def close(self):
        """
        Close threads.
        """
        self._bot_mqtt.stop()

    def enroll_new_bot(self, bot_name: str, team_id: str, bot_id: str = str()) -> str:
        """
        Enroll or re-enroll a bot on the server.
        """
        if not bot_id:
            # Enrolling new bot
            self._bot_id = Rest().enroll_new_bot(team_id, bot_name)
        else:
            # Re-using an existing bot
            self._bot_id = bot_id
        logging.debug(f"[ConnectionManager] AI Bot enrolled: bot_id={self._bot_id}")

        # Requesting rest and brokers connections ids
        self._rest_id = self._request_connection()
        self._is_connection_requested = True

        # Starting MQTT listening thread
        self._bot_mqtt.start()

        # Subscribing to topics and queues
        self._bot_mqtt.subscribe()
        self._bot_stomp.subscribe()

        return self._bot_id

    def update_connection_ids(self, rest_id: str = str(), mqtt_id: str = str(), stomp_id: str = str()):
        """
        Update ids received from the server. These ids are stored in order to send them back to the server and
        validate our connection.
        """
        if rest_id:
            self._rest_id = rest_id
        if stomp_id:
            self._stomp_id = stomp_id
        if mqtt_id:
            self._mqtt_id = mqtt_id

        # If all ids were retrieved, we send them to the server for validation
        logging.debug(f"[ConnectionManager] {str(self._rest_id)}, {str(self._stomp_id)}, {str(self._mqtt_id)}")
        if self._rest_id and self._mqtt_id and self._stomp_id:
            self._all_services_connected = self._send_ids_to_check()

    def _request_connection(self) -> str:
        """
        Request connections ids to send back in order to enable the bot on server side.
        Returns the rest_id.
        MQTT and STOMP ids need to be retrieved from their queues.
        """
        # Calling the webservice will return a rest_id used to validate RestAPI
        rest_id = Rest().request_connection(self._bot_id)
        logging.info(f"[ConnectionManager] rest_id={rest_id}")
        return rest_id

    def _send_ids_to_check(self) -> bool:
        """
        Validate connection by sending all requested ids.
        """
        are_ids_validated = Rest().send_ids_to_check(self._bot_id, self._rest_id, self._mqtt_id, self._stomp_id)
        logging.info(f"[ConnectionManager] Bot connection status: {'OK' if are_ids_validated else 'KO'}")
        return are_ids_validated
