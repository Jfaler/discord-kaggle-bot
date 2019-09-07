import os
import sys
import discord
import random
import kaggle
import i18n
import random

from datetime import datetime as dt
from kaggle.api.kaggle_api_extended import KaggleApi
from discord.ext import commands
from dotenv import load_dotenv
from pytz import timezone

if os.environ.get("PRODUCTION") is None:
    load_dotenv(verbose=True)

i18n.set('locale', os.environ.get('LOCALE'))
i18n.load_path.append('./locale')

api = KaggleApi()
api.authenticate()

# Store discord token in the variable named token
token = os.getenv('DISCORD_TOKEN')

# This will set the command prefix
bot = commands.Bot(command_prefix='!')

# This function will list all current competitions
@bot.command(name='comp', help='Responds with a list of competitions')
async def competitions(comp):
    competition = api.competitions_list()
    response = competition
    await comp.send(response)

# This function will list all datasets
@bot.command(name='datasets', help='Responds with a list of datasets')
async def datasets(ds):
    datasets = api.dataset_list()
    response = datasets
    await ds.send(response)

# This function will list all kernels
@bot.command(name='kernels', help='Responds with a list of kernels')
async def leaderboard(kernels):
    kernel = api.kernels_list()
    response = kernel
    await kernels.send(response)

bot.run(token)
