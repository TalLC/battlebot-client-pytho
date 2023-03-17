from __future__ import annotations

import logging
from queue import SimpleQueue
from battlebotslib.utils.stomp import STOMP
from battlebotslib.common.Messages import Messages
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from battlebotslib.ConnectionManager import ConnectionManager


class StompListener(STOMP.ConnectionListener):

    def on_error(self, frame: STOMP.Frame):
        # Routing errors to messages
        self.on_message(frame)

    @staticmethod
    def on_message(_: STOMP.Frame):
        # Override me pls
        pass


class BotStomp:

    @property
    def queue(self):
        return self._queue

    def __init__(self, connection_manager: ConnectionManager):
        self._connection_manager = connection_manager
        self._queue = SimpleQueue()

        # Listener handling incoming STOMP messages
        self._stomp_listener = StompListener()
        self._stomp_listener.on_message = self._on_message

        # Setting STOMp listener
        STOMP().set_listener("stomp listener", self._stomp_listener)

    def subscribe(self):
        """
        Subscribe to a topic and receive incoming messages.
        """
        # Subscribing to STOMP queue
        STOMP().subscribe(self._connection_manager.bot_id)

    def _on_message(self, frame: STOMP.Frame):
        """
        Callback function on message received from STOMP.
        """
        # Transforming message to dict
        logging.debug("[STOMP] Incoming message")
        message = Messages.message_to_dict(
            frame.body,
            frame.headers['destination'] if 'destination' in frame.headers else str()
        )

        # Checking if the message is a connection id
        if 'msg_type' in message:
            if message['msg_type'] == 'stomp_id':
                self._connection_manager.update_connection_ids(stomp_id=message['data']['value'])
                return

        # Sending message to the internal queue
        self._queue.put(message)
