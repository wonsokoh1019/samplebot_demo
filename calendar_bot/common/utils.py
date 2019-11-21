#!/bin/env python
# -*- coding: utf-8 -*-
"""
HTTP method providing authentication
"""

__all__ = ['auth_post', 'auth_get', 'auth_del', 'auth_del']

import requests
import logging
from tornado.web import HTTPError
from calendar_bot.common.token import generate_token
from calendar_bot.common.global_data import get_value, set_value

LOGGER = logging.getLogger("calendar_bot")


def refresh_token():
    my_token = generate_token()
    set_value("token", my_token)
    return my_token


def get_token():
    return get_value("token", None)


def replace_url_bot_no(url):
    bot_no = get_value("bot_no", None)
    if bot_no is None:
        LOGGER.info("internal error. bot no is None")
        raise HTTPError(500, "internal error. bot no is None")

    url = url.replace("_BOT_NO_", bot_no)
    return url


def auth_post(url, data=None,  headers=None, files=None,
              params=None, json=None, refresh_token_flag=False):
    """
    Encapsulates the post method of adding token to headers.
    Check also: calendar_bot/common/token.py
    parameters and return values, refer to:
    reference: https://3.python-requests.org/user/advanced/#request-and-response-objects
    """

    if headers is not None and not refresh_token_flag:
        my_token = get_token()
        if my_token is None:
            my_token = refresh_token()

        headers["Authorization"] = "Bearer " + my_token
        response = requests.post(url, data=data, headers=headers,
                                 files=files, params=params, json=json)

        if response.status_code == 401 or response.status_code == 403:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
            response = requests.post(url, data=data, headers=headers,
                                     files=files, params=params, json=json)
        return response
    else:
        if refresh_token_flag and headers is not None:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
        return requests.post(url, data=data, headers=headers,
                             files=files, params=params, json=json)

    return None


def auth_get(url, headers=None, refresh_token_flag=False):
    """
    Encapsulates the get method of adding token to headers.
    Check also: calendar_bot/common/token.py
    parameters and return values, refer to:
    reference: https://3.python-requests.org/user/advanced/#request-and-response-objects
    """

    if headers is not None and not refresh_token_flag:
        my_token = get_token()
        if my_token is None:
            my_token = refresh_token()

        headers["Authorization"] = "Bearer " + my_token
        response = requests.get(url, headers=headers)

        if response.status_code == 401 or response.status_code == 403:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
            response = requests.get(url, headers=headers)
        return response
    else:
        if refresh_token_flag and headers is not None:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
        return requests.get(url, headers=headers)

    return None


def auth_del(url, headers=None, refresh_token_flag=False):
    """
    Encapsulates the delete method of adding token to headers.
    Check also: calendar_bot/common/token.py
    parameters and return values, refer to:
    reference: https://3.python-requests.org/user/advanced/#request-and-response-objects
    """

    if headers is not None and not refresh_token_flag:
        my_token = get_token()
        if my_token is None:
            my_token = init_token()

        headers["Authorization"] = "Bearer " + my_token
        response = requests.delete(url, headers=headers)

        if response.status_code == 401 or response.status_code == 403:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
            response = requests.delete(url, headers=headers)
        return response
    else:
        if refresh_token_flag and headers is not None:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
        return requests.delete(url, headers=headers)

    return None


def auth_put(url, data=None,  headers=None, files=None,
              params=None, json=None, refresh_token_flag=False):
    """
    Encapsulates the put method of adding token to headers.
    Check also: calendar_bot/common/token.py
    parameters and return values, refer to:
    reference: https://3.python-requests.org/user/advanced/#request-and-response-objects
    """
    if headers is not None and not refresh_token_flag:
        my_token = get_token()
        if my_token is None:
            my_token = refresh_token()

        headers["Authorization"] = "Bearer " + my_token
        response = requests.put(url, data=data, headers=headers,
                                 files=files, params=params, json=json)

        if response.status_code == 401 or response.status_code == 403:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
            response = requests.put(url, data=data, headers=headers,
                                     files=files, params=params, json=json)
        return response
    else:
        if refresh_token_flag and headers is not None:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
        return requests.put(url, data=data, headers=headers,
                             files=files, params=params, json=json)

    return None
