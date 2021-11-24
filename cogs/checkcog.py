from discord.ext import commands


class checkcog(commands.Cog,name="check"):
    """
    デバッグ用コグ
    """
    def __init__(self,bot):
        self.bot=bot

    @commands.command(description="hello!")
    async def hello(self,ctx):
        """
        動作確認
        """
        await ctx.send("hello!")

    @commands.command(description="userIDcheck")
    async def user(self,ctx):
        """
        ユーザーIDを返すよ
        """
        await ctx.send(ctx.author.id)

    @commands.command(description="send dm")
    async def dm(self,ctx):
        """
        送った人のDMに突撃するよ
        """
        await ctx.author.send("Direct Mail!!")







def setup(bot):
    """
    コグに絶対いるやつ
    """
    print("checkcog OK")
    return bot.add_cog(checkcog(bot))