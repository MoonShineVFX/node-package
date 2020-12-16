import requests
from typing import Union


class Auth:
    def __init__(self, server_url='http://msws-auth-api'):
        """
        Specify auth api server to connect.
        Default value is for docker environment.

        :param server_url: auth api server url .
        """
        if server_url.endswith('/'):
            server_url = server_url[:-1]
        self._server_url = server_url

    def get_token(self, username: str, password: str) -> (bool, str):
        """
        Get auth token by moonshine AD account.

        :param username: AD username.
        :param password: AD password.
        :return: tuple(is_success, token/message).
        """
        resp = requests.post(
            f'{self._server_url}/login',
            auth=(username, password)
        )

        return resp.ok, resp.text

    def validate_token(self, token: str=None) -> (bool, Union[dict, str]):
        """
        Check whether auth token is valid.
        Using cookie instead if token arg not specified.

        :param token: auth token to validate.
        :return: tuple(is_success, {username, token}/message).
        """
        if token is None:
            from flask import request
            cookies = request.cookies
            if 'auth_token' not in cookies:
                return False, 'No token in cookie.'
            token = cookies['auth_token']

        cookies = {'auth_token': token}
        resp = requests.get(
            f'{self._server_url}/validate',
            cookies=cookies
        )

        if resp.ok:
            return True, resp.json()
        return False, resp.text

    def get_user_info(self, token: str=None) -> (bool, Union[dict, str]):
        """
        Get user info by token.
        Using cookie instead if token arg not specified.

        :param token: user info to received.
        :return: tuple(is_success, user_info/message).
        """
        result, data = self.validate_token(token)
        if not result:
            return result, data

        cookies = {'auth_token': data['token']}
        resp = requests.get(
            f'{self._server_url}/user',
            cookies=cookies
        )

        if resp.ok:
            return True, resp.json()
        return False, resp.text
