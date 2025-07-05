import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

puzzle_role = "cruciverbalists"

@bot.event
async def on_ready():
    print(f"Ready to puzzle with {bot.user.name}")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def pingme(ctx):
    role = discord.utils.get(ctx.guild.roles, name=puzzle_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {puzzle_role}")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def dontpingme(ctx):
    role = discord.utils.get(ctx.guild.roles, name=puzzle_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {puzzle_role} removed")
    else:
        await ctx.send("Role doesn't exist")

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

bot.run(token, log_handler=handler, log_level=logging.DEBUG)