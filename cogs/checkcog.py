from discord.ext import commands
from cogs import taskcog

class checkcog(commands.Cog,name="check"):
    def __init__(self,bot):
        self.bot=bot

    @commands.command(description="hello!")
    async def hello(self,ctx):
        await ctx.send("hello!")

    @commands.command(description="userIDcheck")
    async def user(self,ctx):
        await ctx.send(ctx.author.id)

    @commands.command(description="send dm")
    async def dm(self,ctx):
        await ctx.author.send("Direct Mail!!")

    @commands.command(description="userlist")
    async def user_list(self,ctx):
        print(taskcog.users)




def setup(bot):
  print("checkcog OK")
  return bot.add_cog(checkcog(bot))