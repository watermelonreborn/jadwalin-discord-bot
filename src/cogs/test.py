import discord

from discord.ext import commands

from services.guild_service import GuildService

class TestCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.answer = None

    @commands.command()
    async def test(self, ctx, *args):
        await ctx.send(f'Test received.')

    @commands.command()
    async def info(self, ctx, *args):
        channel = await GuildService.get_text_channel(ctx.message.guild.id, ctx.message.channel.id)
        await channel.send(f'Info received from {ctx.message.author.id} in {ctx.message.guild.id}.')

def setup(bot):
    bot.add_cog(TestCommands(bot))
