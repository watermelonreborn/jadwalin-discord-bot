import os
import requests

from dotenv import load_dotenv

from models.reminder import Event

load_dotenv()

class UserService:
    URL = str(os.getenv("BACKEND_URL")) + '/api/user'

    @staticmethod
    async def register_user(register_code, user_id, server_id):
        response = requests.post(UserService.URL + '/code', json={
            'code': str(register_code),
            'discord_id': str(user_id),
            'server_id': str(server_id),
        })

        if response.status_code == 400:
            return 'There was an error on the Discord Bot. Please try again later.'

        if response.status_code == 404:
            return 'The code you entered is invalid. Please try again with a valid code.'

        if response.status_code == 200:
            return 'Successfully registered user.'

        return 'Unexpected error has occured. Please try again later.'

    @staticmethod
    async def unregister_user():
        pass

    @staticmethod
    async def get_settings(user_id, server_id):
        """
        Parameters
        ==========
        arg1: user_id (int)
        arg2: server_id (int)

        Returns
        =======
        settings (dict)
        """
        response = requests.get(UserService.URL + '/settings', json={
            'discord_id': str(user_id),
            'server_id': str(server_id),
        })

        if response.status_code == 200:
            return response.json()['data']

        return None

    @staticmethod
    async def sync_calendar(user_id, server_id):
        """
        Parameters
        ==========
        arg1: user_id (int)
        arg2: server_id (int)

        Returns
        =======
        successful/failed message
        """
        response = requests.post(UserService.URL + '/sync', json={
            'discord_id': str(user_id),
            'server_id': str(server_id),
        })

        if response.status_code == 200:
            return 'Successfully synced calendar.'

        if response.status_code == 404:
            return 'You\'re not registered. Use "register" command for more information.'

        return 'Unexpected error has occured. Please try again later.'

    @staticmethod
    async def get_events(user_id, server_id):
        """
        Parameters
        ==========
        arg1: user_id (int)
        arg2: server_id (int)

        Returns
        =======
        successful/failed message
        """
        response = requests.post(UserService.URL + '/events', json={
            'discord_id': str(user_id),
            'server_id': str(server_id),
        })

        if response.status_code == 200:
            events = response.json()['data']

            if not len(events):
                return 'You don\'t have any listed events.'

            message = f'<@{user_id}>\'s events:\n'
            count = 1

            for e in events:
                event = Event(**e)
                message += f'> {count}. {event.summary}\n'

            return message

        if response.status_code == 404:
            return 'You\'re not registered. Use "register" command for more information.'

        return 'Unexpected error has occured. Please try again later.'

    @staticmethod
    async def get_summary(user_id, server_id):
        """
        Parameters
        ==========
        arg1: user_id (int)
        arg2: server_id (int)

        Returns
        =======
        successful/failed message
        """
        response = requests.post(UserService.URL + '/summary', json={
            'discord_id': str(user_id),
            'server_id': str(server_id),
            'days': 7,
        })

        if response.status_code == 200:
            data = response.json()['data']

            message = f'<@{user_id}> is available on:\n'

            # TODO: Create message for summary

            return message

        if response.status_code == 404:
            return 'You\'re not registered. Use "register" command for more information.'

        return 'Unexpected error has occured. Please try again later.'
