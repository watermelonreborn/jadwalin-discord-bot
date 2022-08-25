import os
import requests

from models.guild import Guild

from dotenv import load_dotenv

load_dotenv()

class GuildService:
    # Guilds is a dict, dict format {"guild_id": Guild}
    guilds = dict()

    bot = None
    URL = str(os.getenv("BACKEND_URL")) + '/api/server'

    @staticmethod
    async def get_or_add_guild(guild_id, text_channel_id):
        if guild_id in GuildService.guilds:
            return GuildService.guilds[guild_id]

        # Fetch guild from backend if doesn't exists
        id, channel = await GuildService.get_guild_from_backend(guild_id)

        if id and channel:
            new_guild = Guild(id, channel)
            GuildService.guilds[id] = new_guild
            return GuildService.guilds[id]

        # Create if doesn't exists in backend
        await GuildService.post_guild_to_backend(guild_id, text_channel_id)

        new_guild = Guild(guild_id, text_channel_id)
        GuildService.guilds[guild_id] = new_guild
        return GuildService.guilds[guild_id]

    @staticmethod
    async def get_text_channel(guild_id, current_text_channel_id):
        guild = await GuildService.get_or_add_guild(guild_id, current_text_channel_id)
        return GuildService.bot.get_channel(guild.get_text_channel_id())

    @staticmethod
    async def set_text_channel(guild_id, text_channel_id):
        guild = await GuildService.get_or_add_guild(guild_id, text_channel_id)
        guild.set_text_channel_id(text_channel_id)

        # Send message to backend to set text channel
        await GuildService.update_guild_to_backend(guild_id, text_channel_id)

        return GuildService.bot.get_channel(guild.get_text_channel_id())

    @staticmethod
    async def get_guild_from_backend(guild_id):
        """
        Parameters
        ==========
        arg1: guild_id (int)

        Returns
        =======
        guild_id (string)
        guild_text_channel (string)
        """
        response = requests.get(GuildService.URL + '/' + str(guild_id))

        if response.status_code == 200:
            data = response.json()['data']
            return int(data['server_id']), int(data['text_channel'])

        return None, None

    @staticmethod
    async def post_guild_to_backend(guild_id, text_channel_id):
        response = requests.post(GuildService.URL + '/create', json={
            'server_id': str(guild_id),
            'text_channel': str(text_channel_id),
        })

        if response.status_code != 200:
            print('[ERROR] An error occured while registering server to backend.')

    @staticmethod
    async def update_guild_to_backend(guild_id, text_channel_id):
        response = requests.post(GuildService.URL + '/update', json={
            'server_id': str(guild_id),
            'text_channel': str(text_channel_id),
        })

        if response.status_code != 200:
            print('[ERROR] An error occured while updating server to backend.')

    # Get text channel strictly by id without error handling
    @staticmethod
    async def get_text_channel_by_id(guild_id):
        if guild_id in GuildService.guilds:
            guild = GuildService.guilds[guild_id]
            return GuildService.bot.get_channel(guild.get_text_channel_id())

        id, channel = await GuildService.get_guild_from_backend(guild_id)

        new_guild = Guild(id, channel)
        GuildService.guilds[guild_id] = new_guild
        return GuildService.bot.get_channel(new_guild.get_text_channel_id())
