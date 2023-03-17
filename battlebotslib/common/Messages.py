import logging
import json


class Messages:

    @staticmethod
    def message_to_dict(msg: str, topic: str) -> dict:
        """
        Transform broker messages to readable Python dict.
        """
        try:
            data = json.loads(msg)
        except json.decoder.JSONDecodeError:
            logging.error(f"Received invalid JSON: {msg}")
            return dict()

        # Logging received message
        logging.debug(f"[BROKER] Received '{data}' from '{topic}' topic")

        return data
