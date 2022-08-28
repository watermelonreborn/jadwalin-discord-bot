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
        channel = await GuildService.get_text_channel(ctx.message.guild.id, ctx.message.channel.id)
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
        channel = await GuildService.get_text_channel(ctx.message.guild.id, ctx.message.channel.id)
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
        channel = await GuildService.set_text_channel(ctx.message.guild.id, ctx.message.channel.id)
        await channel.send("Successfully set default text channel to " + ctx.message.channel.name)

    # Sync calendar for user
    @commands.command()
    async def sync(self, ctx, *args):
        channel = await GuildService.get_text_channel(ctx.message.guild.id, ctx.message.channel.id)
        message = await UserService.sync_calendar(ctx.message.author.id, ctx.message.guild.id)
        await channel.send(message)

    # Send user's event
    @commands.command()
    async def event(self, ctx, *args):
        channel = await GuildService.get_text_channel(ctx.message.guild.id, ctx.message.channel.id)
        message = await UserService.get_events(ctx.message.author.id, ctx.message.guild.id)
        await channel.send(message)

    # Send user's summary
    @commands.command()
    async def summary(self, ctx, *args):
        channel = await GuildService.get_text_channel(ctx.message.guild.id, ctx.message.channel.id)
        message = ''

        days, start_hour, end_hour = 7, 0, 24

        if len(args) >= 1:
            if not args[0].isdigit() or int(args[0]) <= 0:
                await channel.send('Wrong input: days must be an integer greater than 0.')
                return
            
            days = int(args[0])

        if len(args) >= 2:
            if not args[1].isdigit() or int(args[1]) < 0 or int(args[1]) > 24:
                await channel.send('Wrong input: start_hour must be an integer (24 >= start_hour >= 0).')
                return
            
            start_hour = int(args[1])

        if len(args) >= 3:
            if not args[2].isdigit() or int(args[2]) < start_hour or int(args[2]) > 24:
                await channel.send('Wrong input: end_hour must be an integer. (24 >= end_hour >= start_hour')
                return
            
            end_hour = int(args[2])

        message = await UserService.get_summary(ctx.message.author.id, ctx.message.guild.id, days, start_hour, end_hour)
        await channel.send(message)

def setup(bot):
    bot.add_cog(UserCommands(bot))
