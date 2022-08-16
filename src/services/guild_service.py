from models.guild import Guild

class GuildService:
    # Guilds is a dict, dict format {"guild_id": Guild}
    guilds = dict()

    @staticmethod
    def get_or_add_guild(guild_id):
        if guild_id in GuildService.guilds:
            return GuildService.guilds[guild_id]

        # TODO: Fetch guild from backend if doesn't exists
        else:
            new_guild = Guild(guild_id)
            GuildService.guilds[guild_id] = new_guild
            return GuildService.guilds[guild_id]

    @staticmethod
    def get_text_channel(bot, guild_id, current_text_channel_id):
        guild = GuildService.get_or_add_guild(guild_id)
        if not guild.get_text_channel_id():
            # TODO: Fetch text channel from backend if doesn't exists and set if backend returns None
            guild.set_text_channel_id(current_text_channel_id)
        return bot.get_channel(guild.get_text_channel_id())

    @staticmethod
    def set_text_channel(bot, guild_id, text_channel_id):
        guild = GuildService.get_or_add_guild(guild_id)
        guild.set_text_channel_id(text_channel_id)
        # TODO: Send message to backend to set text channel
        return bot.get_channel(guild.get_text_channel_id())
