<link rel="stylesheet" type="text/css" href="../style/style.css">

<!-- Side navigation -->
<div class="sidebar">
  <center><img src="../img/Python-logo-notext.svg"></center>
  <h1>Sommaire</h1>
  
  <a href="../Battlebotslib%20-%20Python.html">Battlebotslib - Python</a>
  <ul>
    <li><a href="Installation%20de%20la%20lib%20Python.html">Installation de la lib Python</a></li>
	  <li><a href="../tech/Classe%20BotAi.html">Classe BotAi</a></li>
  </ul>
</div>

<!-- Page content -->
<div class="main">


# Installation de la lib Python

Vous devez avoir obtenu le fichier `battlebotslib.zip` au préalable. Ce fichier contient la bibliothèque Python à installer via PIP dans votre projet d'IA.

## Installation

### Environnement virtuel

Il est recommandé de vous créer un environnement virtuel au sein de votre projet d'IA et de l'activer avant d'installer la bibliothèque et ses dépendances.

Pour créer un environnement virtuel Python :
- `python -m venv venv`

Activer l'environnement virtuel :
- Windows :
  - `venv\Scripts\activate.bat`
- Linux :
  - `source venv/bin/activate`

Installer la lib :
- `pip install dist\battlebotslib-0.5.2-py3-none-any.whl`


### Configuration de la lib

Pour que la lib fonctionne, il faut créer 3 fichiers de configuration qui vont donner les informations de connexions aux différents services.

Ils sont à créer dans votre projet d'IA Python, dans un sous-dossier `conf`.

Voici les fichiers avec les informations pour vous connecter à votre serveur local :

**conf/rest.json**
```json
{
  "host": "localhost",
  "port": 8000,
  "protocol": "http"
}
```

**conf/mqtt.json**
```json
{
  "destination_root": "BATTLEBOT/BOT/",
  "username": "user",
  "password": "password",
  "host": "localhost",
  "port": 1883,
  "connect_timeout": 5
}
```

**conf/stomp.json**
```json
{
  "destination_root": "BATTLEBOT.BOT.",
  "username": "user",
  "password": "password",
  "host": "localhost",
  "port": 61613
}
```


Vous êtes prêt à utiliser la bibliothèque.

La classe principale permettant d'interagir avec votre IA est `battlebotslib.BotAi`.

---

[⬆️ Retour](#top) - _Installation de la lib Python_

</div>
