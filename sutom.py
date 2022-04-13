from email.message import Message
from time import time
from discord import Embed
from discord import Color
from discord import Game
from discord.ext import commands
from dotenv import load_dotenv
import datetime
import pymongo
import threading
import pytz
import os

from process import *

load_dotenv()

mongodb = pymongo.MongoClient(os.getenv("MONGO_URL"), tz_aware = True)
createDate = datetime.datetime(2022, 1, 7)
timezone = pytz.timezone("Europe/Paris")
print(datetime.datetime.now(tz = timezone))

bot = commands.Bot(command_prefix = '$')

@bot.event
async def on_ready():
    print("Bot ready")
    await bot.change_presence(activity = Game(name = "Sutom - $aide"))
    checkTime()

@bot.event
async def on_message(message: Message):
    await bot.process_commands(message)
    if message.content.startswith("SUTOM #"):
        now = datetime.datetime.now(tz = timezone) + datetime.timedelta(hours = 2)
        print(now)
        delta = now.date() - createDate.date()
        if not str(delta.days) in message.content:
            await message.add_reaction("❌")
            return
        
        sutomCode = decodeSutom(message.content)
        print(sutomCode)
        if not verifySutom(sutomCode):
            await message.add_reaction("❌")
            return
        
        score = scoreSutom(sutomCode)

        print("score : ", score)

        db = mongodb[str(message.guild.id)].score
        verify = db.find_one({"userId": message.author.id}, sort=[( '_id', pymongo.DESCENDING )])
        if verify is not None:
            date = datetime.datetime.date(verify["date"])
            if date == now.date():
                print("même jour !")
                await message.add_reaction("❌")
                return

        send = {
            "userId": message.author.id,
            "userName": message.author.name,
            "score": score,
            "schematic": sutomCode,
            "date": now
        }
        db = mongodb[str(message.guild.id)].score
        result = db.insert_one(send)

        db = mongodb[str(message.guild.id)].users

        result = db.find_one({"userId": message.author.id})

        if result is None:
            send = {
                "userId": message.author.id,
                "userName": message.author.name,
                "score": score,
                "completed": 1,
                "created": now,
                "lastUpdate": now
            }
            result = db.insert_one(send)
        else:
            newScore = result['score'] + score
            newCompleted = result['completed'] + 0
            if score != 0:
                newCompleted = result['completed'] + 1
            result = db.update_one({"userId": message.author.id}, {"$set": {
                "score": newScore,
                "completed": newCompleted,
                "lastUpdate": now
            }})

        switcher = {
            6: "Incroyable ! Du premier coup ! **+6 points**",
            5: "Génial ! Tu as trouvé en 2 essais ! **+5 points**",
            4: "Bien joué ! Tu as trouvé le mots en 3 coups ! **+4 points**",
            3: "GG Tu as trouvé le mot ! **+3 points**",
            2: "Pas mal, essaye de faire mieux demain ! **+2 points**",
            1: "Wouah ! Tu as trouvé au dernier essai ! **+1 point**",
            0: "Dommage... Retente le coup demain ! **+0 points**"
        }

        stringResult = switcher.get(score, lambda: "Score non valide")
        await message.channel.send(stringResult)
        await message.add_reaction("✅")

@bot.command()
async def score(ctx):
    db = mongodb[str(ctx.message.guild.id)].users
    result = db.find_one({"userId": ctx.author.id})
    if result is None:
        await ctx.send("Aucun score enregistré.")
        return
    
    embed = Embed(
        title = "Résultats Sutom de " + result["userName"] + " :",
        color = Color.red()
    )

    embed.set_author(
        name = ctx.author.name,
        icon_url = ctx.author.avatar_url
    )

    embed.add_field(
        name = "Score total",
        value = result["score"],
        inline = True
    )

    embed.add_field(
        name = "Sutom complétés",
        value = result["completed"]
    )

    await ctx.send(embed = embed)

@bot.command()
async def top(ctx):
    db = mongodb[str(ctx.message.guild.id)].users
    result = db.find(sort = [( 'score', pymongo.DESCENDING )], limit = 10)

    if result is None:
        await ctx.send("Aucun joueur enregistré")
        return

    first = result[0]

    description = ""
    i = 0
    for user in result:
        i += 1
        description += "**" + str(i) + ". " + user["userName"] + "** " + str(user["score"]) + " points | " + str(user["completed"]) + " complétés\n"

    embed = Embed(
        title = "Top 10 du serveur",
        description = description,
        color = Color.gold()
    )
    
    user = await bot.fetch_user(first["userId"])
    embed.set_thumbnail(url = user.avatar_url)

    await ctx.send(embed = embed)

@bot.command()
async def aide(ctx):
    await ctx.send(
        "Bienvenue sur le **Bot Sutom**. \n" +
        "Copiez / Collez votre résultat Sutom dans ce channel pour enregistrer votre score. \n" +
        "**Attention, vous ne pouvez enregistrer qu'un résultat par jour et évitez la triche...**\n\n" +
        "Commandes disponibles :\n" +
        "**$score** - Affiche votre score global\n" +
        "**$top** - Affiche le top score du serveur\n" +
        "**$aide** - Affiche cette aide LUL\n\n" +
        "Bot développé par **Thibma**"
    )

# Disponible uniquement sur mon serveur pour le moment (en cours pour tous les serveurs)
def checkTime():
    threading.Timer(1, checkTime).start()
    now = pytz.utc.localize(datetime.datetime.now()).astimezone(timezone).strftime("%H:%M:%S")

    if(now == '00:00:00'):  # check if matches with the desired time
        print("send daily message")
        channel = bot.get_channel(953643248939860048) # mettez l'ID de votre channel discord
        bot.loop.create_task(channel.send(
            "**Sutom du jour disponible ! Bonne chance !**\n\n" +
            "https://sutom.nocle.fr"
        ))



bot.run(os.getenv("TOKEN_BOT"))