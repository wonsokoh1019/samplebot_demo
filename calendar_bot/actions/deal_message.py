#!/bin/env python
# -*- coding: utf-8 -*-
"""
deal user input messages
"""

__all__ = ['deal_user_message', 'deal_message']

import tornado.web
import time
import logging
from tornado.web import HTTPError
from calendar_bot.common.local_timezone import local_date_time
from calendar_bot.externals.send_message import push_messages
from calendar_bot.actions.message import invalid_message, error_message
from calendar_bot.actions.direct_sign_in import deal_sign_in
from calendar_bot.actions.direct_sign_out import deal_sign_out
from calendar_bot.model.processStatusDBHandle import get_status_by_user, \
    set_status_by_user_date

LOGGER = logging.getLogger("calendar_bot")


@tornado.gen.coroutine
def deal_user_message(account_id, current_date, create_time, message):
    """
    Process messages entered by users,
    Different scenarios need different processing functions.
    Please see the internal implementation of the handler.

    :param account_id: user account id.
    :param current_date: current date by local time.
    :param create_time: Time when the user requests to arrive at the BOT server.
    :param message: User entered message.
    :return: message content
    """

    date_time = local_date_time(create_time)

    content = get_status_by_user(account_id, current_date)

    if content is None or content[0] is None:
        LOGGER.info("status is None account_id:%s message:%s content:%s",
                    account_id, message, str(content))
        raise HTTPError(403, "Messages not need to be processed")

    status = content[0]
    process = content[1]
    try:
        user_time = int(message)
    except Exception:
        if status == "wait_in" or status == "wait_out":
            return error_message()
        else:
            raise HTTPError(403, "Messages not need to be processed")

    tm = date_time.replace(hour=int(user_time / 100),
                           minute=int(user_time % 100))
    user_time_ticket = int(tm.timestamp())

    if (status == "wait_in" or status == "wait_out") \
            and (user_time < 0 or user_time > 2400):
        return error_message()

    if status == "wait_in":
        content = yield deal_sign_in(account_id,
                                     current_date, user_time_ticket, True)
        set_status_by_user_date(account_id, current_date, status="in_done")
        return [content]
    if status == "wait_out":
        content = yield deal_sign_out(account_id,
                                      current_date, user_time_ticket, True)
        set_status_by_user_date(account_id, current_date, status="out_done")
        return [content]
    if process == "sign_in_done" or process == "sign_out_done":
        return [invalid_message()]

    LOGGER.info("can't deal this message account_id:%s message:%s status:%s",
                account_id, message, status)
    raise HTTPError(403, "Messages not need to be processed")


@tornado.gen.coroutine
def deal_message(account_id, current_date, create_time, message):
    """
    Process messages manually entered by the user.

    :param account_id: user account id.
    :param current_date: current date by local time.
    :param create_time: Time the request arrived at the server.
    :param callback: User triggered callback.
    :return: None
    """

    contents = yield deal_user_message(account_id, current_date,
                                       create_time, message)

    yield push_messages(account_id, contents)
