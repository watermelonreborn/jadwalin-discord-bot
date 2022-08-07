import discord

from discord.ext import commands

from services.guild_service import GuildService

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Register user to application if token received
    # Send application's URL if token not received
    @commands.command()
    async def register(self, ctx, *args):
        channel = GuildService.get_text_channel(self.bot, ctx.message.guild.id, ctx.message.channel.id)
        if len(args) == 0:
            await channel.send("Please provide a token from our website ...")
            return

        # TODO: Register user to application via backend

    # Send user's settings for current server
    @commands.command()
    async def settings(self, ctx, *args):
        pass

def setup(bot):
    bot.add_cog(UserCommands(bot))
