import os
import requests

class UserService:
    URL = str(os.getenv("BACKEND_URL")) + '/api/user'

    @staticmethod
    async def register_user(register_code, user_id, server_id):
        response = requests.post(UserService.URL + '/code', json={
            'code': register_code,
            'discord_id': user_id,
            'server_id': server_id,
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
            'discord_id': user_id,
            'server_id': server_id,
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
        response = requests.get(UserService.URL + '/sync', json={
            'discord_id': user_id,
            'server_id': server_id,
        })

        if response.status_code == 200:
            return 'Successfully synced calendar.'

        if response.status_code == 404:
            return 'You\'re not registered. Use "register" command for more information.'

        return 'Unexpected error has occured. Please try again later.'
