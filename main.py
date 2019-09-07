# bot.py
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
    now = dt.now()
    now = now.astimezone(timezone('UTC'))
    await comp.send(i18n.t('kaggle.hi', hour=now.hour))
    competitions_list = api.competitions_list()
    for competition in competitions_list:
        if getattr(competition, 'awardsPoints') and not getattr(competition, 'submissionsDisabled'):
            deadline = getattr(competition, 'deadline')
            deadline = deadline.astimezone(timezone('UTC'))
            diff = deadline - now
            if diff.days > 0:
                await comp.send('{}: {}'.format(i18n.t('kaggle.to_go', days=diff.days), getattr(competition, 'title')))

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

# This function will list all kernels
@bot.command(name='lb', help='Responds with Leaderboard')
async def files(ctx):
    ctx = api.competitions_submissions_list()
    response = random.choice(ctx)
    await ctx.send(response)


bot.run(token)
