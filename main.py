import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

import datetime # for puzzles by date
from typing import Literal # for autocomplete
import re # for date format checking

import puzzle_utils


class Client(commands.Bot):
    async def on_ready(self):
        print(f"Ready to puzzle with {self.user.name}")

        try:
            load_dotenv()
            guild = discord.Object(id=os.getenv('TEST_SERVER_ID'))
            await self.tree.sync(guild=GUILD_ID)
            print(f"Synced commands to guild {guild.id}")
        except Exception as e:
            print(f"Error syncing commands: {e}")

        
# setup logger and intents
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = Client(command_prefix='!', intents=intents) # prefix sorta irrelevant, not used


# pull values from .env
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
puzzle_role = os.getenv("PUZZLE_ROLE")
guildID = os.getenv('TEST_SERVER_ID')

GUILD_ID = discord.Object(id=guildID)


@client.tree.command(name="pingme", description="change if you get pinged when a puzzle is posted", guild=GUILD_ID)
async def pingme(interaction: discord.Interaction, toggle: Literal["yes", "no"]):
    role = discord.utils.get(interaction.guild.roles, name=puzzle_role)
    if role:
        if toggle == "yes":
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{interaction.user.mention} will now be pinged for puzzles", ephemeral = True)
        else:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"{interaction.user.mention} will no longer be pinged for puzzles", ephemeral = True)
    else:
        await interaction.response.send_message("Role doesn't exist")

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
            puzzleName = puzzle_utils.getPuzzleName(publisher, puzzleDate)
        else:
            puzzleName = puzzle_utils.getPuzzleName(publisher)

        await interaction.response.send_message(await puzzle_utils.makeGame(searchTerm = puzzleName))

    except Exception as e:
        print(f"Error getting results: {e}")


client.run(token, log_handler=handler, log_level=logging.DEBUG)