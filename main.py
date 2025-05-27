import collections
import discord
import asyncpg
from discord.ext import commands
import json
import asyncio
from pymongo import MongoClient
import os


intents = discord.Intents.all()
client = commands.Bot(command_prefix = ['d.','D.'], case_insensitive = True, intents = intents)
cluster = MongoClient()
database = cluster['discord']
collection = database["faction"]
faction = database["wars"]
client.remove_command('help')

os.chdir(r"C:\Users\Hi\Documents\codes\Coding\database")

@client.event
async def on_ready():
    print('Ready')

@client.command(name = 'ping')
async def ping_command(ctx):
    await ctx.send(f'Pong! **{int(client.latency * 1000)}ms**')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = '**Cooldown**, please try again in {:.2f}s'.format(error.retry_after)

        await ctx.send(msg)

extensions = ['cogs.ClanCommands', 'cogs.GambleCommands', 'cogs.HelpCommands', 'cogs.Minigames', 'cogs.MiscCommands']

if __name__ == '__main__':
    for ext in extensions: 
        client.load_extension(ext)

client.run("####")