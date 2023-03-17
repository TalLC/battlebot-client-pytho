import json
from pathlib import Path
from battlebotslib.conf.RestConfig import RestConfig
from battlebotslib.conf.MQTTConfig import MQTTConfig
from battlebotslib.conf.STOMPConfig import STOMPConfig

# Config files
CONFIG_REST = RestConfig(**json.loads(Path('conf/rest.json').read_text()))
CONFIG_MQTT = MQTTConfig(**json.loads(Path('conf/mqtt.json').read_text()))
CONFIG_STOMP = STOMPConfig(**json.loads(Path('conf/stomp.json').read_text()))
