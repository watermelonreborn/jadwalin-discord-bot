import asyncio

class MessageService:
    loop = asyncio.get_event_loop()

    # Send message using synchrounous function
    @staticmethod
    def send(text_channel, message):
        MessageService.loop.create_task(text_channel.send(message))