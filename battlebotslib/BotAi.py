from battlebotslib.utils.rest import Rest, RestException
from battlebotslib.ConnectionManager import ConnectionManager
from queue import Empty

class BotAi:

    RestException: RestException = RestException

    @property
    def bot_id(self):
        return self.connection_manager.bot_id

    def __init__(self, bot_name: str, team_id: str):
        self._bot_name = bot_name
        self._team_id = team_id
        self.connection_manager = ConnectionManager()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """
        Close threads.
        """
        self.connection_manager.close()

    def enroll(self, bot_id: str = str()) -> str:
        """
        Enroll or re-enroll a bot on the server.
        Giving an existing bot id allows you to connect this bot without adding a new one to the game.
        """
        return self.connection_manager.enroll_new_bot(self._bot_name, self._team_id, bot_id)

    def read_scanner(self, block=True) -> dict:
        """
        Read and remove one item from the scanner queue.
        Example, two trees are detected:
        {
          "msg_type": "object_detection",
          "source": "scanner",
          "data": [
            {
              "from": 26.5,
              "to": 31,
              "name": "Tree",
              "distance": 6.844473640068633
            },
            {
              "from": 34,
              "to": 39.5,
              "name": "Tree",
              "distance": 5.777348380771669
            }
          ]
        }
        """
        try:
            return self.connection_manager.mqtt_queue.get(block=block)
        except Empty:
            return dict()

    def read_game_message(self, block=True) -> dict:
        """
        Read and remove one item from the game messages queue.
        Example, your bot cannot move anymore:
        {
          "msg_type": "moving_status",
          "source": "bot",
          "data": {
            "value": false
          }
        }
        """
        try:
            return self.connection_manager.stomp_queue.get(block=block)
        except Empty:
            return dict()

    def move(self, state: bool):
        """
        Start or stop moving the bot forward.
        """
        state_str = "start" if state else "stop"
        Rest().bot_action_move(self.bot_id, state_str)

    def turn(self, direction: str):
        """
        Start or stop turning the bot in one direction.
        Accepted values: left, right, stop
        """
        Rest().bot_action_turn(self.bot_id, direction)

    def shoot(self, angle: float):
        """
        Shoot at the desired angle.
        Accepted value: and angle in degrees.
        """
        Rest().bot_action_shoot(self.bot_id, angle)
