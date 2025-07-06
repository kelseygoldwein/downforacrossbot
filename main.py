import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

import requests # for api calls
import datetime # for puzzles by date
from typing import Literal # for autocomplete
import re # for date format checking

# setup logger and intents
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# pull secret numbers from .env file
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD_ID = discord.Object(id=os.getenv('TEST_SERVER_ID'))
    

class Client(commands.Bot):
    async def on_ready(self):
        print(f"Ready to puzzle with {self.user.name}")

        try:
            getPuzzleName("nyt")
            load_dotenv()
            guild = discord.Object(id=os.getenv('TEST_SERVER_ID'))
            synced = await self.tree.sync(guild=GUILD_ID)
            print(f"Synced commands to guild {guild.id}")
        except Exception as e:
            print(f"Error syncing commands: {e}")

        

# prefix sorta irrelevant, not used
client = Client(command_prefix='!', intents=intents)

puzzle_role = "cruciverbalists"


@client.tree.command(name="pingme", description="get pinged when a puzzle is posted", guild=GUILD_ID)
async def pingme(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, name=puzzle_role)
    if role:
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"{interaction.user.mention} is a {puzzle_role}")
    else:
        await interaction.response.send_message("Role doesn't exist")

@client.tree.command(name="dontpingme", description="stop getting pinged when a puzzle is posted", guild=GUILD_ID)
async def dontpingme(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, name=puzzle_role)
    if role:
        await interaction.user.remove_roles(role)
        await interaction.response.send_message(f"{interaction.user.mention} is not a {puzzle_role}")
    else:
        await interaction.response.send_message("Role doesn't exist")


# TODO send as embeds not links


@client.tree.command(name="puzzle", description="start a puzzle", guild=GUILD_ID)
async def startPuzzle(interaction: discord.Interaction, 
                        publisher: Literal["nyt", "lat", "usa", "wsj", "newsday", "universal", "atlantic"],
                        date: str = ""):
    try:
        dateFormat = re.compile(r"^[0-1]?\d\/[0-3]?\d(\/[1-2]\d\d\d)?$")
        
        if dateFormat.match(date):
            dateParts = date.split("/")
            year = datetime.date.today().year if len(dateParts) == 2 else int(dateParts[2])

            puzzleDate = datetime.date(year, int(dateParts[0]), int(dateParts[1]))
            puzzleName = getPuzzleName(publisher, puzzleDate)
        else:
            puzzleName = getPuzzleName(publisher)

        await interaction.response.send_message(await makeGame(searchTerm = puzzleName))

    except Exception as e:
        print(f"Error getting results: {e}")


async def getResults(resultsPage = 0, pageSize = 50, searchTerm = "", standardSize = "true", miniSize = "true"):

    response = requests.get(f"https://api.foracross.com/api/puzzle_list?"
                            f"page={resultsPage}&"
                            f"pageSize={pageSize}&"
                            f"filter%5BnameOrTitleFilter%5D={searchTerm}&"
                            f"filter%5BsizeFilter%5D%5BMini%5D={miniSize}&"
                            f"filter%5BsizeFilter%5D%5BStandard%5D={standardSize}"
                            ) 
    responseJson = response.json()
    if len(responseJson["puzzles"]) == 0:
        print(f"oops, no results found for {searchTerm}")
        return None
    return responseJson

async def getPuzzleID(results, index = 0):
    try:
        return results["puzzles"][index]["pid"]

    except Exception as e:
        print(f"Error getting results: {e}")

async def getGID():
    gidCounter = requests.post("https://api.foracross.com/api/counters/gid")
    gidCounterJson = gidCounter.json()
    return gidCounterJson["gid"]

async def createGame(pid, gid):
    data = {"gid":gid, "pid":pid}
    requests.post("https://api.foracross.com/api/game", json=data)

def getGameURL(gid):
    return f"https://downforacross.com/beta/game/{gid}"

async def makeGame(resultsPage = 0, pageSize = 50, searchTerm = "", standardSize = "true", miniSize = "true"):
    results = await getResults(resultsPage, pageSize, searchTerm, standardSize, miniSize)
    if results == None:
        return "no puzzles found"
    puzzleID = await getPuzzleID(results)
    gameID = await getGID()
    await createGame(puzzleID, gameID)
    return getGameURL(gameID)

def getPuzzleName(publisher, date=datetime.date.today()):
    match publisher:
        case "nyt":
            return date.strftime(f"NY Times, %A, %B {date.day}, %Y")
        case "lat":
            return date.strftime(f"L. A. Times, %a, %b {date.day}, %Y")
        case "usa":
            return date.strftime(f"USA Today %A, %b %d, %Y")
        case "wsj":
            return date.strftime(f"WSJ %A, %b %d, %Y")
        case "newsday":
            return date.strftime(f"Newsday %A, %b %d, %Y")
        case "universal":
            return date.strftime(f"Universal Crossword %A")
        case "atlantic":
            return date.strftime(f"Atlantic %A, %b %d, %Y")
        case _:
            print(f"error for publisher {publisher}")
            return ""
    

client.run(token, log_handler=handler, log_level=logging.DEBUG)