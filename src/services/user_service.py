import os
import requests

from dotenv import load_dotenv

from models.reminder import Event
from models.summary import Summary

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
            count = 0

            for e in events:
                event = Event(**e)
                count += 1

                if event.start_time.date_time.strftime("%H:%M") == '00:00' and event.end_time.date_time.strftime("%H:%M"):
                    message += f'> {count}. {event.summary} {event.start_time.date_time.strftime("(%d %b %Y)")}\n'
                    continue

                message += f'> {count}. {event.summary} {event.start_time.date_time.strftime("(%d %b %Y, %H:%M-") + event.end_time.date_time.strftime("%H:%M)")}\n'

            return message

        if response.status_code == 404:
            return 'You\'re not registered. Use "register" command for more information.'

        return 'Unexpected error has occured. Please try again later.'

    @staticmethod
    async def get_summary(user_id, server_id, days, start_hour, end_hour):
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
            'days': days - 1,
            'start_hour': start_hour,
            'end_hour': end_hour,
        })

        if response.status_code == 200:
            summaries = response.json()['data']

            message = f'<@{user_id}> is available on:\n'

            for s in summaries:
                summary = Summary(**s)
                message += f'> {summary.date.strftime("%d %b %Y")}:'

                for time in summary.availability:
                    message += f' {time.start_hour}:00-{time.end_hour}:00,'

                message = message[:-1] + '\n'

            return message

        if response.status_code == 404:
            return 'You\'re not registered. Use "register" command for more information.'

        return 'Unexpected error has occured. Please try again later.'
