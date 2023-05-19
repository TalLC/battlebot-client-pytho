import logging
from dataclasses import dataclass
from battlebotslib.BotAi import BotAi
from Events import BotHealthStatusMessage, BotStunningStatusMessage
from Events import BotMovingSpeedStatusMessage, BotMovingStatusMessage
from Events import BotTurningSpeedStatusMessage, BotTurningStatusMessage
from Events import BotWeaponStatusMessage, BotWeaponCooldownMessage


@dataclass
class Weapon:
    # damages = 5
    can_shoot = True
    cooldown = 0

    def __str__(self) -> str:
        return f"Weapon cooldown (ms)={self.cooldown}\n" \
               f"Weapon can shoot={self.can_shoot}"


@dataclass
class BotState:
    is_stunned = False
    is_turning = False
    direction = ''
    is_moving = False

    def __str__(self) -> str:
        return f"Is stunned={self.is_stunned}\n" \
               f"Is turning={self.is_turning} (direction='{self.direction}')\n" \
               f"Is moving={self.is_moving}"


class Bot:

    @property
    def id(self) -> str:
        return self._bot_id

    @property
    def health(self) -> int:
        return self._health

    @property
    def moving_speed(self) -> float:
        return self._moving_speed

    @property
    def turning_speed(self) -> float:
        return self._turning_speed

    @property
    def state(self) -> BotState:
        return self._state

    @property
    def weapon(self) -> Weapon:
        return self._weapon

    def __init__(self, name: str, team_id: str):
        self.must_stop = False
        self._health = 999
        self._moving_speed = 0
        self._turning_speed = 0
        self._state = BotState()
        self._weapon = Weapon()
        self._api = BotAi(name, team_id)
        self._bot_id = self._api.enroll()

    def update(self, message: BotHealthStatusMessage | BotStunningStatusMessage |
                              BotMovingSpeedStatusMessage | BotMovingStatusMessage |
                              BotTurningSpeedStatusMessage | BotTurningStatusMessage |
                              BotWeaponStatusMessage | BotWeaponCooldownMessage):
        if isinstance(message, BotHealthStatusMessage):
            self._health = message.health
        elif isinstance(message, BotStunningStatusMessage):
            self._state.is_stunned = message.is_stunned
        elif isinstance(message, BotMovingSpeedStatusMessage):
            self._moving_speed = message.moving_speed
        elif isinstance(message, BotMovingStatusMessage):
            self._state.is_moving = message.is_moving
        elif isinstance(message, BotTurningSpeedStatusMessage):
            self._turning_speed = message.turning_speed
        elif isinstance(message, BotTurningStatusMessage):
            self._state.is_turning = False if message.turning_status == 'stop' else True
            self._state.direction = '' if message.turning_status == 'stop' else message.turning_status
        elif isinstance(message, BotWeaponStatusMessage):
            self._weapon.can_shoot = message.can_shoot
        elif isinstance(message, BotWeaponCooldownMessage):
            self._weapon.cooldown = message.cooldown

    def get_stats(self):
        return "BOT :\n" \
              f"Health={self.health}\n" \
              f"Moving speed={self.moving_speed}\n" \
              f"Turning speed={self.turning_speed}\n" \
              f"STATE :\n" \
              f"{self.state}\n" \
              f"WEAPON :\n" \
              f"{self.weapon}"

    def read_scanner(self) -> dict:
        return self._api.read_scanner(block=False)

    def read_game_message(self) -> dict:
        return self._api.read_game_message(block=False)

    def shoot(self, angle: float):
        if not self.state.is_stunned:
            self._api.shoot(angle)

    def move(self):
        if not self.state.is_moving and not self.state.is_stunned:
            self._api.move(True)

    def stop(self):
        if self.state.is_moving:
            self._api.move(False)

    def turn(self, direction: str):
        if direction == 'stop' and self.state.is_turning:
            self._api.turn(direction)
        elif direction != 'stop' and self.state.direction != direction and \
                not self.state.is_turning and \
                not self.state.is_stunned:
            self._api.turn(direction)
