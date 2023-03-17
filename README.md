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
