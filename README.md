# Documentation
- [Installation de la lib](docs/client/Installation%20de%20la%20lib%20Python.md)
- [Utilisation de la classe BotAi](docs/tech/Classe%20-%20BotAi.md)

# Build du package de la lib

## Créer un venv dans ce dossier (battlebotslib-sources)
```
python3 -m venv venv
```

## Activer l'environnement
```
venv\Scripts\activate.bat
```

## Installer les prérequis au build
```
pip install wheel setuptools twine
```

## Build la lib
```
python setup.py bdist_wheel
```

# Installation de la lib

## Commande d'installation
```
pip install dist\battlebotslib-0.4.0-py3-none-any.whl
```

# IA de test
## Pré-requis
Un script Python d'IA de test a été créée pour illustrer l'utilisation de la lib cliente.  
Un fichier `requirements.txt` est fourni et il faut avoir la lib client installée pour utiliser cette IA.
- [Code source](example)

## Configuration
- [Config du bot](example/bot1.json) (nom et id d'équipe)
- [Informations de connexions](example/conf) (Rest, STOMP et MQTT)

