import discord

from discord.ext import commands

class TestCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.answer = None

    @commands.command()
    async def test(self, ctx, *args):
        await ctx.send(f'Test received from {ctx.message.guild.id}')

def setup(bot):
    bot.add_cog(TestCommands(bot))
