import os
import requests

class UserService:
    URL = os.getenv("BACKEND_URL") + '/api/user'

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

    @staticmethod
    async def unregister_user():
        pass
