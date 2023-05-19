import logging
from typing import Any
from BrokerMessage import BrokerMessage


class Event(BrokerMessage):

    @property
    def source(self) -> str:
        return self._source

    def __init__(self, message: dict):
        self._msg_type = message['msg_type']
        self._source = message['source']
        self._value = message['data']['value']

    @staticmethod
    def get(message: dict) -> Any:
        if len(message.keys()) > 0:
            if Event.is_valid_message(message):
                match message['msg_type']:
                    case 'game_status':
                        return GameStatusMessage(message)
                    case 'health_status':
                        return BotHealthStatusMessage(message)
                    case 'moving_speed_status':
                        return BotMovingSpeedStatusMessage(message)
                    case 'turning_speed_status':
                        return BotTurningSpeedStatusMessage(message)
                    case 'stunning_status':
                        return BotStunningStatusMessage(message)
                    case 'moving_status':
                        return BotMovingStatusMessage(message)
                    case 'turning_status':
                        return BotTurningStatusMessage(message)
                    case 'weapon_can_shoot':
                        return BotWeaponStatusMessage(message)
                    case 'weapon_cooldown_ms':
                        return BotWeaponCooldownMessage(message)
                    case _:
                        logging.error(f"Message d'événement de type inconnu : \n{message}")
                        return None
            else:
                logging.error(f"Message d'événement malformé : \n{message}")
                return None
        return None

    @staticmethod
    def get_mandatory_fields() -> [str]:
        return ['msg_type', 'source', 'data']

    @staticmethod
    def is_valid_message(message: dict) -> bool:
        for field in Event.get_mandatory_fields():
            if field not in message:
                return False
        return True


class GameStatusMessage(Event):
    """
    Informe le client du démarrage et de l'arrêt de la partie.
    """
    @property
    def is_started(self) -> bool:
        return self._value

    def __init__(self, message: dict):
        super().__init__(message)


class BotMovingSpeedStatusMessage(Event):
    """
    Donne la vitesse de déplacement max actuelle du bot.
    """
    @property
    def moving_speed(self) -> float:
        return self._value

    def __init__(self, message: dict):
        super().__init__(message)


class BotHealthStatusMessage(Event):
    """
    Donne le nombre de PV du bot.
    """
    @property
    def health(self) -> int:
        return self._value

    def __init__(self, message: dict):
        super().__init__(message)


class BotTurningSpeedStatusMessage(Event):
    """
    Donne la vitesse de rotation max actuelle du bot.
    """
    @property
    def turning_speed(self) -> float:
        return self._value

    def __init__(self, message: dict):
        super().__init__(message)


class BotWeaponCooldownMessage(Event):
    """
    Temps de recharge de l'arme entre chaque tir.
    """
    @property
    def cooldown(self) -> bool:
        return self._value

    def __init__(self, message: dict):
        super().__init__(message)


class BotStunningStatusMessage(Event):
    """
    État d'étourdissement du bot.
    """
    @property
    def is_stunned(self) -> bool:
        return self._value

    def __init__(self, message: dict):
        super().__init__(message)


class BotMovingStatusMessage(Event):
    """
    État de déplacement du bot.
    """
    @property
    def is_moving(self) -> bool:
        return self._value

    def __init__(self, message: dict):
        super().__init__(message)


class BotTurningStatusMessage(Event):
    """
    État de rotation du bot.
    """
    @property
    def turning_status(self) -> str:
        return self._value

    def __init__(self, message: dict):
        super().__init__(message)


class BotWeaponStatusMessage(Event):
    """
    État de l'arme du bot.
    """
    @property
    def can_shoot(self) -> bool:
        return self._value

    def __init__(self, message: dict):
        super().__init__(message)
