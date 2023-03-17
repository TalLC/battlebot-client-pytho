<link rel="stylesheet" type="text/css" href="../style/style.css">
<link rel="stylesheet" type="text/css" href="../style/dark-theme.css">
<link rel="stylesheet" type="text/css" href="../style/dark-code.css">

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

Il est recommandé de vous créer un environnement virtuel au sein de votre projet et de l'activer avant d'installer la bibliothèque et ses dépendances.

Pour créer un environnement virtuel Python :
- `python -m venv venv`

Activer l'environnement virtuel :
- Windows :
  - `venv\Scripts\activate.bat`
- Unix :
  - `source venv/Scripts/activate`

Installer la lib :
- `pip install dist\battlebotslib-0.4.0-py3-none-any.whl`


Après l'installation, vous êtes prêt à utiliser la bibliothèque.

La classe principale permettant d'interagir avec votre IA est `battlebotslib.BotAi`.

---

[⬆️ Retour](#top) - _Installation de la lib Python_

</div>
