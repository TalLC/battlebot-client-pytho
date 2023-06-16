import sys
import json
import logging
from datetime import timedelta
from time import time, sleep
from pathlib import Path
from threading import Thread, Event
from queue import SimpleQueue, Empty
from battlebotslib.BotAi import BotAi
import Events
from Events import GameStatusMessage
from DetectedObject import DetectedObject
from Bot import Bot


#
# Appel du script
# python main.py [botx.json]
#


# Bot config
# Si un fichier de config est fourni en entrée, on l'utilise, sinon on prend 'bot1.json'
if len(sys.argv) > 1:
    conf_file = sys.argv[1]
else:
    conf_file = 'bot1.json'
G_BOT_CONFIG = json.loads(Path(conf_file).read_text())

# Game
G_GAME_IS_STARTED = False

# Fight
G_BORDER_DETECTED = False
G_TARGET_BOT_QUEUE = SimpleQueue()
G_TARGET_DESTRUCTIBLES_QUEUE = SimpleQueue()
G_TURN_DIRECTION = 'right'

# Multithreading
# - Thread events
G_SCANNER_EVENT = Event()
G_EVENT_EVENT = Event()


def stop():
    """
    Closing messages reading threads.
    """
    global G_SCANNER_EVENT
    global G_EVENT_EVENT

    G_SCANNER_EVENT.set()
    G_EVENT_EVENT.set()


def thread_read_scanner_messages(e: Event, _bot: Bot):
    """
    Thread continuously reading messages from the broker's scanner queue.
    """
    global G_BORDER_DETECTED

    _border_distance = 2.0
    _bot_distance = 9.0
    _destructible_distance = 5.0

    while not e.is_set():
        if G_GAME_IS_STARTED:
            detected_objects_message = _bot.read_scanner()
            if 'timestamp' in detected_objects_message:
                logging.info(f"[SCANNER] Message received in {timedelta(seconds=time() - detected_objects_message['timestamp'])}")
            
            detected_objects = list(DetectedObject.get(detected_objects_message))

            if len(detected_objects):
                detected_borders = [
                    x for x in detected_objects
                    if x.name.lower() in ['desintegrator', 'water', 'rock', 'tree', 'bot'] and x.distance <= _border_distance
                ]
                if len(detected_borders):
                    G_BORDER_DETECTED = True
                else:
                    G_BORDER_DETECTED = False

                detected_bots = [
                    x for x in detected_objects
                    if x.object_type.lower() == 'bot' and x.distance <= _bot_distance
                ]
                for detected_bot in detected_bots:
                    G_TARGET_BOT_QUEUE.put_nowait(detected_bot)

                detected_destructibles = [
                    x for x in detected_objects
                    if x.object_type.lower() not in ['bot', 'tile', 'rock'] and x.distance <= _destructible_distance
                ]
                for detected_destructible in detected_destructibles:
                    G_TARGET_DESTRUCTIBLES_QUEUE.put_nowait(detected_destructible)


def thread_read_event_messages(e: Event, _bot: Bot):
    """
    Thread continuously reading messages from the broker's event queue.
    """
    global G_GAME_IS_STARTED

    while not e.is_set():
        event_message = _bot.read_game_message()
        if 'timestamp' in event_message:
            logging.info(f"[EVENT] Message received in {timedelta(seconds=time() - event_message['timestamp'])}")
        
        event = Events.Event.get(event_message)
        if event:
            if isinstance(event, GameStatusMessage):
                G_GAME_IS_STARTED = event.is_started
            else:
                _bot.update(event)


if __name__ == "__main__":
    # Logging
    logging.basicConfig(level=logging.INFO, datefmt='%d/%m/%Y %I:%M:%S',
                        format='[%(levelname)s] %(asctime)s - %(message)s')

    # Creating a new Bot
    bot = Bot(G_BOT_CONFIG['bot_name'], G_BOT_CONFIG['team_id'])

    # Bot scanner messages handler process
    Thread(target=thread_read_scanner_messages, args=(G_SCANNER_EVENT, bot)).start()

    # Game messages handler process
    Thread(target=thread_read_event_messages, args=(G_EVENT_EVENT, bot)).start()

    # Waiting for the game to start
    while not G_GAME_IS_STARTED:
        sleep(0.1)

    # Game is started
    logging.info(bot.get_stats())

    try:

        # Big AI time
        while bot.health > 0 and G_GAME_IS_STARTED:
            try:
                # Stop moving if close to border
                if G_BORDER_DETECTED:
                    bot.stop()
                else:
                    bot.move()

                # Shooting
                if bot.weapon.can_shoot:
                    if not G_TARGET_BOT_QUEUE.empty():
                        bot.stop()
                        bot.turn('stop')
                        while not G_TARGET_BOT_QUEUE.empty():
                            try:
                                target = G_TARGET_BOT_QUEUE.get(block=False)
                                bot.shoot((target.angle_to + target.angle_from) / 2)
                                if abs(target.angle_from) > abs(target.angle_to):
                                    G_TURN_DIRECTION = 'left'
                                else:
                                    G_TURN_DIRECTION = 'right'
                            except Empty:
                                pass
                    elif not G_TARGET_DESTRUCTIBLES_QUEUE.empty():
                        bot.stop()
                        bot.turn('stop')
                        while not G_TARGET_DESTRUCTIBLES_QUEUE.empty():
                            try:
                                target = G_TARGET_DESTRUCTIBLES_QUEUE.get(block=False)
                                bot.shoot((target.angle_to + target.angle_from) / 2)
                            except Empty:
                                pass
                    else:
                        bot.turn(G_TURN_DIRECTION)

            except BotAi.RestException as ex:
                pass

            sleep(1 / 1000)

        # Game has stopped or the bot is dead
        if bot.health <= 0:
            logging.info("Bot is dead")

        elif not G_GAME_IS_STARTED:
            logging.info("Game has been stopped")
        stop()

    except KeyboardInterrupt:
        logging.info("Bot has been aborted")
        stop()
