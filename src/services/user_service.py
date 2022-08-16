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

        # TODO: handle success message
        if response.status_code == 200:
            return 'Successfully registered user'

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
