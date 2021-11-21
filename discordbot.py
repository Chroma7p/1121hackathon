
import discord
import textwrap
from discord.ext import commands,tasks
import datetime

bot=commands.Bot(command_prefix='!')
cogfolder="cogs."
cogs=["checkcog",
      "taskcog"]



for c in cogs:
  bot.load_extension(cogfolder+c)

tc=bot.get_cog("taskcog")



with open("token.txt","r")as f:
  TOKEN=f.read().replace("\n","")

    




@bot.event
async def on_ready():
    print("Hello!")
    await bot.change_presence(activity=discord.Game(name="test", type=1))


bot.run(TOKEN)