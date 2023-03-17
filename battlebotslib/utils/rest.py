import json
import logging
import requests
from battlebotslib.common.config import CONFIG_REST
from battlebotslib.common.Singleton import SingletonABCMeta


class RestException(Exception):
    def __init__(self, name: str, internal_code: int, label: str):
        self.name = name
        self.internal_code = internal_code
        self.label = label

    def __str__(self):
        return f"{self.name} ({hex(self.internal_code)}) {self.label}"


class Rest(metaclass=SingletonABCMeta):

    rest_server = f"{CONFIG_REST.protocol}://{CONFIG_REST.host}:{CONFIG_REST.port}"

    def __init__(self):
        self._http_session = requests.session()

    def _send_to_rest(self, endpoint: str, method: str, payload: dict = None) -> dict:
        """
        Send an HTTP request to Rest API.
        """
        if method.lower() == "post":
            requests_func = self._http_session.post
        elif method.lower() == "patch":
            requests_func = self._http_session.patch
        elif method.lower() == "put":
            requests_func = self._http_session.put
        else:
            requests_func = self._http_session.get

        r = requests_func(f"{self.rest_server}{endpoint}", json=payload if payload is not None else dict())

        if r.ok:
            return r.json()
        else:
            try:
                if 'detail' in r.json():
                    # Raising a RestException using values from details
                    raise RestException(**r.json()['detail'])
            except json.JSONDecodeError:
                pass
            
        logging.error(f"[REST] {method.lower()} {endpoint} - Bad response from Rest API:\n"
                      f"Response: {r.status_code} - {r.text}")

    def enroll_new_bot(self, team_id: str, bot_name: str) -> str:
        """
        Enroll a new bot in a team.
        """
        method = "post"
        endpoint = "/bots/action/register"
        payload = {
            'team_id': team_id,
            'bot_name': bot_name
        }
        data = self._send_to_rest(endpoint, method, payload)

        return data['bot_id']

    def request_connection(self, bot_id: str) -> str:
        """
        Request identifiers for Rest, Stomp and MQTT.
        """
        method = "get"
        endpoint = f"/bots/{bot_id}/action/request_connection"
        data = self._send_to_rest(endpoint, method)

        return data['request_id']

    def send_ids_to_check(self, bot_id: str, rest_id: str, mqtt_id: str, stomp_id: str) -> bool:
        """
        Request identifiers for Rest, Stomp and MQTT.
        """
        method = "patch"
        endpoint = f"/bots/{bot_id}/action/check_connection"
        payload = {
            'rest_id': rest_id,
            'mqtt_id': mqtt_id,
            'stomp_id': stomp_id
        }
        data = self._send_to_rest(endpoint, method, payload)

        # Check if the ids were validated by the server
        if 'status' in data:
            if data['status'] == 'ok':
                return True

        return False

    def bot_action_move(self, bot_id: str, state: str):
        """
        Start or stop moving the bot forward.
        Accepted values: start, stop
        """
        method = "patch"
        endpoint = f"/bots/{bot_id}/action/move"
        payload = {
            "action": state
        }
        self._send_to_rest(endpoint, method, payload)

    def bot_action_turn(self, bot_id: str, direction: str):
        """
        Start or stop turning the bot in one direction.
        Accepted values: left, right, stop
        """
        method = "patch"
        endpoint = f"/bots/{bot_id}/action/turn"
        payload = {
            "direction": direction
        }
        self._send_to_rest(endpoint, method, payload)

    def bot_action_shoot(self, bot_id: str, angle: float):
        """
        Shoot at the desired angle.
        Accepted value: and angle in degrees.
        """
        method = "patch"
        endpoint = f"/bots/{bot_id}/action/shoot"
        payload = {
            "angle": angle
        }
        self._send_to_rest(endpoint, method, payload)
