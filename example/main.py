import sys
import json
import logging
import random
from datetime import datetime, timedelta
from time import sleep
from pathlib import Path
from threading import Event, Thread
from battlebotslib.BotAi import BotAi
from queue import SimpleQueue

# Bot config
G_BOT_ID_TMP_FILE = Path('bot_id.tmp')
G_BOT_CONFIG = json.loads(Path('bot1.json').read_text())

# Game information
G_GAME_IS_STARTED = False

# Bot information
G_BOT_HEALTH: int = 999     # Depends on the bot type, we need to read this information from the game messages
G_BOT_IS_MOVING: bool = False
G_BOT_IS_TURNING: bool = False
G_BOT_TURN_DIRECTION: str = str()
G_BOT_IS_STUNNED: bool = False
G_WEAPON_CAN_SHOOT: bool = True

# Will be used to store all the objects to shoot at
G_BOT_TARGETS_QUEUE: SimpleQueue = SimpleQueue()


def check_for_existing_bot_id() -> str:
    """
    If a bot was previously registered, we read the bot_id.
    """
    if G_BOT_ID_TMP_FILE.exists():
        return G_BOT_ID_TMP_FILE.read_text()
    else:
        return ""


def thread_read_scanner_queue(e: Event, bot_ai: BotAi):
    """
    Thread continuously reading messages from the bot scanner queue.
    """
    while not e.is_set():
        scanner_message = bot_ai.read_scanner()
        logging.debug(f"[SCANNER] {scanner_message}")
        handle_scanner_message(scanner_message)


def thread_read_game_queue(e: Event, bot_ai: BotAi):
    """
    Thread continuously reading messages from the game queue.
    """
    while not e.is_set():
        game_message = bot_ai.read_game_message()
        logging.debug(f"[GAME] {game_message}")
        handle_game_message(game_message)


def handle_scanner_message(message: dict):
    """
    Handle a new scanner message.
    """
    try:
        if message['msg_type'] == "object_detection":
            # Browsing detected objects
            for detected_object in message['data']:
                is_valid_target = False
                target = None
                match detected_object['object_type']:
                    # We want to shoot at trees and bots
                    case "tree":
                        is_valid_target = True
                        target = detected_object
                    case "bot":
                        is_valid_target = True
                        target = detected_object
                    # We cannot walk on water
                    case "tile":
                        if detected_object["name"].lower() == "water":
                            logging.debug("WATER WATER WATER!!!")
                    case _:
                        pass

                if is_valid_target:
                    target_angle = (target['from'] + target['to']) / 2
                    logging.info(f"[SCANNER] {target['name']} detected at a distance of "
                                 f"{target['distance']} ({target_angle}°)")
                    G_BOT_TARGETS_QUEUE.put(target_angle)
        else:
            logging.error(f"Unknown scanner message: {message}")
    except:
        logging.error(f"Bad scanner message format: {message}")


def handle_game_message(message: dict):
    """
    Handle a new game message.
    """
    try:
        match message['msg_type']:
            case "health_status":
                global G_BOT_HEALTH
                # Bot health update
                G_BOT_HEALTH = message['data']['value']
                show_bot_stats()
            case "game_status":
                global G_GAME_IS_STARTED
                # Game is running or stopped
                G_GAME_IS_STARTED = message['data']
            case "stunning_status":
                global G_BOT_IS_STUNNED
                # Bot is stunned or not
                G_BOT_IS_STUNNED = message['data']['value']
            case "moving_status":
                global G_BOT_IS_MOVING
                # Bot is moving or not
                G_BOT_IS_MOVING = message['data']['value']
            case "turning_status":
                global G_BOT_IS_TURNING
                global G_BOT_TURN_DIRECTION
                if message['data']['value'] == 'stop':
                    # Bot has been stopped
                    G_BOT_IS_TURNING = False
                else:
                    # Turn direction
                    G_BOT_IS_TURNING = True
                    G_BOT_TURN_DIRECTION = message['data']['value']
            case "weapon_can_shoot":
                global G_WEAPON_CAN_SHOOT
                G_WEAPON_CAN_SHOOT = message['data']['value']
            case _:
                logging.error(f"Unknown game message: {message}")
    except:
        logging.error(f"Bad game message format: {message}")


def get_opposite_direction(direction: str) -> str:
    if direction.lower() == 'left':
        return 'right'
    elif direction.lower() == 'right':
        return 'left'
    else:
        return 'stop'


def show_bot_stats():
    logging.info(f"Health: {G_BOT_HEALTH}")


if __name__ == "__main__":
    # Logging
    logging.basicConfig(level=logging.DEBUG, datefmt='%d/%m/%Y %I:%M:%S',
                        format='[%(levelname)s] %(asctime)s - %(message)s')

    # Creating a new Bot
    with BotAi(G_BOT_CONFIG['bot_name'], G_BOT_CONFIG['team_id']) as bot:
        def stop():
            # Closing messages reading threads
            scanner_message_thread_event.set()
            game_message_thread_event.set()

            # Removing temp file
            G_BOT_ID_TMP_FILE.unlink(missing_ok=True)

        # Bot enrollment
        try:
            # If we crashed after enrolling the bot, we re-use the same bot_id if it was stored
            bot_id = bot.enroll(check_for_existing_bot_id())
        except BotAi.RestException as ex:
            # If the bot id is invalid
            if ex.name == 'BOT_DOES_NOT_EXISTS':
                # Bot id was invalid, deleting tmp file
                G_BOT_ID_TMP_FILE.unlink(missing_ok=True)
                # Enrolling as new bot
                bot_id = bot.enroll()
            else:
                logging.exception(str(ex))
                sys.exit()

        # Writing new bot id to tmp file
        G_BOT_ID_TMP_FILE.write_text(bot_id)

        # Bot scanner messages handler thread
        scanner_message_thread_event = Event()
        Thread(target=thread_read_scanner_queue, args=(scanner_message_thread_event, bot)).start()

        # Game messages handler thread
        game_message_thread_event = Event()
        Thread(target=thread_read_game_queue, args=(game_message_thread_event, bot)).start()

        # Randomize directions and durations
        rand_gen = random.Random()

        # Waiting for the game to start
        while not G_GAME_IS_STARTED:
            sleep(0.1)

        # Game is started
        show_bot_stats()

        try:
            # Big AI time

            last_turn_ts = datetime.now()
            while G_BOT_HEALTH > 0 and G_GAME_IS_STARTED:
                try:
                    if not G_BOT_TARGETS_QUEUE.empty():
                        bot.shoot(G_BOT_TARGETS_QUEUE.get(block=False))

                    if not G_BOT_IS_MOVING:
                        bot.move(True)

                    if not G_BOT_IS_TURNING:
                        bot.turn(rand_gen.choice(['left', 'right']))
                    elif G_BOT_IS_TURNING and datetime.now() - last_turn_ts > timedelta(seconds=5):
                        bot.turn(rand_gen.choice(['left', 'right']))
                        last_turn_ts = datetime.now()

                except BotAi.RestException as ex:
                    pass

            # Game has stopped or the bot is dead
            if G_BOT_HEALTH <= 0:
                logging.info("Bot is dead")

            elif not G_GAME_IS_STARTED:
                logging.info("Game has been stopped")
            stop()

        except KeyboardInterrupt:
            logging.info("Bot has been aborted")
            stop()
