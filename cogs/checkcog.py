from discord.ext import commands

class checkcog(commands.Cog,name="check"):
    def __init__(self,bot):
        self.bot=bot

    @commands.command(description="hello!")
    async def hello(self,ctx):
        await ctx.send("hello!")


def setup(bot):
  print("checkcog OK")
  return bot.add_cog(checkcog(bot))