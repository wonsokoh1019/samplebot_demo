#!/bin/env python
# -*- coding: utf-8 -*-
"""
rich menu's api
"""

__all__ = ['upload_content', 'make_add_rich_menu_body', 'set_rich_menu_image',
           'set_user_specific_rich_menu', 'get_rich_menus',
           'cancel_user_specific_rich_menu', 'init_rich_menu']

import io
import logging
import json
from calendar_bot.model.data import make_size, make_bound, i18n_display_text, \
    make_i18n_label, make_postback_action, make_add_rich_menu, make_area
from calendar_bot.common import utils
from calendar_bot.constant import API_BO, OPEN_API, RICH_MENUS
import tornado.gen
from calendar_bot.common.utils import auth_get, auth_post, auth_del

LOGGER = logging.getLogger("calendar_bot")


def upload_content(file_path):
    """
    Upload rich menu background picture.
    reference: https://developers.worksmobile.com/kr/document/1005025?lang=en

    :param file_path: resource local path
    :return: resource id
    """
    headers = {
        "consumerKey": OPEN_API["consumerKey"],
        "x-works-apiid": OPEN_API["apiId"]
    }

    files = {'resourceName': open(file_path, 'rb')}

    url = API_BO["upload_url"]
    url = utils.replace_url_bot_no(url)

    LOGGER.info("upload content . url:%s", url)

    response = auth_post(url, files=files, headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("upload content. http return error.")
    if "x-works-resource-id" not in response.headers:
        LOGGER.error("invalid content. url:%s txt:%s headers:%s",
                    url, response.text, response.headers)
        raise Exception("upload content. not fond 'x-works-resource-id'.")
    return response.headers["x-works-resource-id"]


def make_add_rich_menu_body(rich_menu_name):
    """
    add rich menu body
    reference: https://developers.worksmobile.com/kr/document/100504001?lang=en

    :param rich_menu_name: rich menu name
    :return: rich menu id
    """
    size = make_size(2500, 1686)

    bound0 = make_bound(0, 0, 1250, 1286)
    action0 = make_postback_action("sign_in",
                                   display_text="Record clock-in",
                                   label="Record clock-in",)

    bound1 = make_bound(1250, 0, 1250, 1286)
    action1 = make_postback_action("sign_out",
                                   display_text="Record clock-out",
                                   label="Record clock-out")

    bound2 = make_bound(0, 1286, 2500, 400)
    action2 = make_postback_action("to_first",
                                   display_text="Start over",
                                   label="Start over")

    rich_menu = make_add_rich_menu(
                    rich_menu_name,
                    size,
                    [
                        make_area(bound0, action0),
                        make_area(bound1, action1),
                        make_area(bound2, action2)
                    ])

    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]

    url = API_BO["rich_menu_url"]
    url = utils.replace_url_bot_no(url)

    LOGGER.info("register richmenu. url:%s", url)

    response = auth_post(url, data=json.dumps(rich_menu), headers=headers)
    if response.status_code != 200:
        LOGGER.info("register richmenu failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("register richmenu. http return error.")

    LOGGER.info("register richmenu success. url:%s txt:%s body:%s",
                url, response.text, response.content)

    tmp = json.loads(response.content)
    return tmp["richMenuId"]


def set_rich_menu_image(resource_id, rich_menu_id):
    """
    Set a rich menu image.
    reference: https://developers.worksmobile.com/kr/document/100504002?lang=en

    :param resource_id: resource id
    :param rich_menu_id: rich menu id
    :return:
    """
    body = {"resourceId": resource_id}

    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]

    url = API_BO["rich_menu_url"] + "/" + rich_menu_id + "/content"
    url = utils.replace_url_bot_no(url)
    LOGGER.info("set rich menu image . url:%s", url)

    response = auth_post(url, data=json.dumps(body), headers=headers)
    if response.status_code != 200:
        LOGGER.info("set rich menu image failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("set richmenu image. http return error.")

    LOGGER.info("set rich menu image success. url:%s txt:%s body:%s",
                url, response.text, response.content)


def set_user_specific_rich_menu(rich_menu_id, account_id):
    """
    Set a user-specific rich menu.
    reference: https://developers.worksmobile.com/kr/document/100504010?lang=en

    :param rich_menu_id: rich menu id
    :param account_id: user account id
    """
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    url = API_BO["rich_menu_url"] + "/" \
          + rich_menu_id + "/account/" + account_id

    url = utils.replace_url_bot_no(url)

    response = auth_post(url, headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("set user specific richmenu. http return error.")
    LOGGER.info("set user specific richmenu success. url:%s txt:%s body:%s",
                url, response.text, response.content)


def get_rich_menus():
    """
    Get rich menus
    reference: https://developers.worksmobile.com/kr/document/100504004?lang=en

    :return: rich menu list
    """
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    url = API_BO["rich_menu_url"]
    url = utils.replace_url_bot_no(url)

    LOGGER.info("push message begin. url:%s", url)
    response = auth_get(url, headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        return None

    LOGGER.info("push message success. url:%s txt:%s body:%s",
                url, response.text, response.content)

    tmp = json.loads(response.content)
    if "richmenus" in tmp:
        return tmp["richmenus"]

    return None


def cancel_user_specific_rich_menu(account_id):
    """
    Cancel a user-specific rich menu
    reference: https://developers.worksmobile.com/kr/document/100504012?lang=en

    :param account_id: user account id
    """
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    url = API_BO["rich_menu_url"] + "/account/" + account_id
    url = utils.replace_url_bot_no(url)

    response = auth_del(url, headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("canncel user specific richmenu. http return error.")
    LOGGER.info("push message success. url:%s txt:%s body:%s",
                url, response.text, response.content)


def init_rich_menu():
    """
    init rich menu.
    reference: https://developers.worksmobile.com/kr/document/1005040?lang=en

    :return: rich menu id
    """
    rich_menus = get_rich_menus()
    if rich_menus is not None:
        for menu in rich_menus:
            if str(menu["name"]) == RICH_MENUS["name"]:
                return  menu["richMenuId"]

    rich_menu_id = make_add_rich_menu_body(RICH_MENUS["name"])
    resource_id = upload_content(RICH_MENUS["path"])
    set_rich_menu_image(resource_id, rich_menu_id)
    return rich_menu_id
