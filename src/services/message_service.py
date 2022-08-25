import asyncio

from models.reminder import Reminder
from services.guild_service import GuildService

from typing import List

class MessageService:
    loop = asyncio.get_event_loop()

    # Send message using synchrounous function
    @staticmethod
    def send(text_channel, message):
        MessageService.loop.create_task(text_channel.send(message))

    # TODO: Beautify message
    @staticmethod
    async def send_reminder(reminders: List[Reminder]):
        for reminder in reminders:
            message = f'<@{reminder.discord_id}>\'s schedule for the next {reminder.hours} hour(s)\n'
            count = 1

            for event in reminder.events:
                message += f'> {count}. {event.summary}\n'
                count += 1

            channel = await GuildService.get_text_channel_by_id(reminder.server_id)
            MessageService.loop.create_task(channel.send(message))
