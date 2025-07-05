import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

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


# pull secret numbers from .env file
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD_ID = discord.Object(id=os.getenv('TEST_SERVER_ID'))
    
# setup logger and intents
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# prefix sorta irrelevant, not used
client = Client(command_prefix='!', intents=intents)

### END SETUP ###



puzzle_role = "cruciverbalists"

@client.tree.command(name="hello", description="say hello!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello!")

@client.tree.command(name="pingme", description="get pinged when a puzzle is posted", guild=GUILD_ID)
async def pingme(ctx):
    role = discord.utils.get(ctx.guild.roles, name=puzzle_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {puzzle_role}")
    else:
        await ctx.send("Role doesn't exist")

@client.tree.command(name="dontpingme", description="stop getting pinged when a puzzle is posted", guild=GUILD_ID)
async def dontpingme(ctx):
    role = discord.utils.get(ctx.guild.roles, name=puzzle_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {puzzle_role} removed")
    else:
        await ctx.send("Role doesn't exist")



client.run(token, log_handler=handler, log_level=logging.DEBUG)


### OLD CODE STARTS HERE, JUST REFERENCE ###
# @bot.command()
# async def dm(ctx, *, msg):
#     await ctx.author.send(f"You said {msg}")

# @bot.command()
# async def reply(ctx):
#     await ctx.reply("This is a reply to your message!")

# @bot.command()
# async def poll(ctx, *, question):
#     embed = discord.Embed(title="New Poll", description=question)
#     poll_message = await ctx.send(embed=embed)
#     await poll_message.add_reaction("👍")
#     await poll_message.add_reaction("👎")

# @bot.command()
# @commands.has_role(puzzle_role)
# async def secret(ctx):
#     await ctx.send("Welcome to the club!")

# @secret.error
# async def secret_error(ctx, error):
#     if isinstance(error, commands.MissingRole):
#         await ctx.send("You do not have permission to do that!")