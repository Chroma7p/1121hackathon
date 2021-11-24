
import discord
from discord.ext import commands


#botの設定
bot=commands.Bot(command_prefix='!')

#コグのフォルダの位置
cogfolder="cogs."
#コグのリスト
cogs=[#"checkcog",#デバッグ用コグ
      "taskcog"]


#各コグの読み込み
for c in cogs:
  bot.load_extension(cogfolder+c)


#discordbotのトークン読み込み(GitHubにトークン上げないため)
with open("token.txt","r")as f:
  TOKEN=f.read().replace("\n","")

    



#起動時の設定
@bot.event
async def on_ready():
    print("Hello!")
    await bot.change_presence(activity=discord.Game(name="test", type=1))#activityでXXをプレイ中って出せる


#起動
bot.run(TOKEN)