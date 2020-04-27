import os
import sys
import discord
import random
import kaggle
import i18n
from datetime import datetime as dt
from kaggle.api.kaggle_api_extended import KaggleApi
from kaggle.api_client import ApiClient
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

# This function will list all 🏆 current competitions
@bot.command(name='competitions', help='Responds with a list of competitions')
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

# This function will list all datasets sorted by 💪 active
@bot.command(name='datasets', help='Responds with a list of datasets sorted by active')
async def datasets(ds):
    await ds.send(i18n.t('kaggle.datasets'))
    datasets = api.dataset_list(sort_by='active')
    response = datasets
    await ds.send('\n'.join('{}: {}'.format(*response) for response in enumerate(response)))

# This function will list all 🏥 health datasets sorted by hottest
@bot.command(name='health', help='Responds with a list of datasets sorted by hottest')
async def heatlh(healthDataset):
    await healthDataset.send(i18n.t('kaggle.health'))
    hDatasets = api.dataset_list(tag_ids='health', sort_by='hottest')
    response = hDatasets
    await healthDataset.send('\n'.join('{}: {}'.format(*response) for response in enumerate(response)))

# This function will list all 💼 education datasets sorted by hottest
@bot.command(name='education', help='Responds with a list of computing related datasets sorted by hottest')
async def education(edu):
    await edu.send(i18n.t('kaggle.education'))
    edu = api.dataset_list(tag_ids='education', sort_by='hottest')
    response = edu
    await edu.send('\n'.join('{}: {}'.format(*response) for response in enumerate(response)))

# This function will list all kernels sorted by hotness 🔥
@bot.command(name='kernels', help='Responds with a list of kernels sorted by hotness')
async def kernel(kernels):
    await kernels.send(i18n.t('kaggle.kernels'))
    kernel = api.kernels_list(page_size=50, sort_by='hotness')
    response = kernel
    await kernels.send('\n'.join('{}: {}'.format(*response) for response in enumerate(response)))

bot.run(token)
