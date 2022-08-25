import discord

from discord.ext import commands

from services.guild_service import GuildService
from services.user_service import UserService

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Register user to application if token received
    # Send application's URL if token not received
    @commands.command()
    async def register(self, ctx, *args):
        channel = await GuildService.get_text_channel(self.bot, ctx.message.guild.id, ctx.message.channel.id)
        if len(args) == 0:
            await channel.send("Please provide a token from our website ...")
            return

        code = args[0]
        message = await UserService.register_user(code, ctx.message.author.id, ctx.message.guild.id)
        await channel.send(message)

    # Unregister user from application
    # TODO: Implement

    # Send user's settings for current server
    @commands.command()
    async def settings(self, ctx, *args):
        channel = await GuildService.get_text_channel(self.bot, ctx.message.guild.id, ctx.message.channel.id)
        if len(args) == 0:
            settings = await UserService.get_settings(ctx.message.author.id, ctx.message.guild.id)
            if settings is None:
                await channel.send('An unexpected error occured. Make sure you are registered to this application, use "register" command for more information.')
                return

            response = '> <@%d>\'s settings:\n' % ctx.message.author.id
            for k, v in settings.items():
                response += '> ' + k + ': ' + str(v) + '\n'

            await channel.send(response)
            return

        # TODO: Implement change settings
        pass

    # Set current text channel as default text channel
    @commands.command()
    async def channel(self, ctx, *args):
        channel = await GuildService.set_text_channel(self.bot, ctx.message.guild.id, ctx.message.channel.id)
        await channel.send("Successfully set default text channel to " + ctx.message.channel.name)

    # Sync calendar for user
    @commands.command()
    async def sync(self, ctx, *args):
        channel = await GuildService.get_text_channel(self.bot, ctx.message.guild.id, ctx.message.channel.id)
        message = await UserService.sync_calendar(ctx.message.author.id, ctx.message.guild.id)
        await channel.send(message)

    # Send user's event
    # TODO: Implement
    @commands.command()
    async def event(self, ctx, *args):
        pass
        # channel = await GuildService.get_text_channel(self.bot, ctx.message.guild.id, ctx.message.channel.id)

def setup(bot):
    bot.add_cog(UserCommands(bot))
