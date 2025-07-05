import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

import requests # for api calls

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
            load_dotenv()
            guild = discord.Object(id=os.getenv('TEST_SERVER_ID'))
            synced = await self.tree.sync(guild=GUILD_ID)
            print(f"Synced commands to guild {guild.id}")
        except Exception as e:
                print(f"Error syncing commands: {e}")

# prefix sorta irrelevant, not used
client = Client(command_prefix='!', intents=intents)

puzzle_role = "cruciverbalists"
response = requests.get("https://api.foracross.com/api/puzzle_list?page=0&pageSize=50&filter%5BnameOrTitleFilter%5D=&filter%5BsizeFilter%5D%5BMini%5D=true&filter%5BsizeFilter%5D%5BStandard%5D=true") 
print(response.status_code)


@client.tree.command(name="hello", description="say hello!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello!")

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

@client.tree.command(name="puzzlelink", description="send link to downforacross", guild=GUILD_ID)
async def puzzleLink(interaction: discord.Interaction):
    await interaction.response.send_message("https://downforacross.com/")

@client.tree.command(name="nyt", description="send link to today's nyt puzzle", guild=GUILD_ID)
async def puzzleLink(interaction: discord.Interaction):
    await interaction.response.send_message("https://downforacross.com/")


client.run(token, log_handler=handler, log_level=logging.DEBUG)