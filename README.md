# Bot SUTOM pour Discord
Bot permettant de jouer entre amis ou communauté sur Discord au jeu SUTOM disponible à l'adresse : https://sutom.nocle.fr/ 

## Crédits
SUTOM crée par [@Jonamaths](https://twitter.com/Jonamaths) inspiré par le jeu Wordle. (Sans lui pas de jeu !)

Bot crée par [@Thibma](https://twitter.com/Thibma_).

## Fonctionnalités
* Lecture des résultats Sutom
* Top 10 du serveur discord
* Score de l'utilisateur
* Mises à jours futures

## Installation

### Prérequis
* [Python 3](https://www.python.org/downloads/)
* Créez une base de donnée MongoDB en local ou sur MongoDB Atlas : https://www.mongodb.com

* Créez un Bot sur la plateforme de développeur Discord : https://discord.com/developers/applications

Téléchargez le projet en le clonant sur votre poste :
```bash
git clone https://github.com/Thibma/SutomDiscordBot.git
```

### En local


Affectez les variables d\'environnement dans un fichier .env:
```bash
mkdir .env

nano .env
```
Dans le fichier '.env' : (Enlevez les '<>') 
```
MONGO_URL=<Adresse de la base de donnée>
TOKEN_BOT=<Token du bot Discord>
```
Installez les dépendances :
```bash
pip3 install -r requirements.txt
```

Puis enfin lancez le script Python :
```bash
python3 sutom.py
```
Le message 'Bot Ready' s'affiche dans la console si tout fonctionne.

### En Production
Il est possible d'héberger le bot sur des plateformes en ligne comme [Heroku](https://www.heroku.com)

Dans ces cas là, il vous faut créer un projet sur Heroku puis dans 'Settings' ajoutez python en 'Buildpacks'.

Ensuite ajoutez les variables d'environnements dans 'Reveal Config Vars' 

```
MONGO_URL : Adresse de la base de donnée
TOKEN_BOT : Token du bot Discord
```

Allez dans 'Deploy' ensuite et suivez les insctructions pour uploadez le Bot sur Heroku.

## Commandes
* `$score` : Affiche le score du joueur
* `$top`: Affiche le Top 10 du serveur
* `$aide` : Affiche l'aide du bot

