Procfile
========

https://devcenter.heroku.com/articles/procfile:

    Heroku apps include a Procfile that specifies the commands that are executed by the app on startup. You can use a Procfile to declare a variety of process types, including:
    
    - Your app’s web server
    - Multiple types of worker processes
    - A singleton process, such as a clock
    - Tasks to run before a new release is deployed

This bot's Procfile:

.. literalinclude:: ../Procfile
    :caption: Procfile



Initialize environment
======================

.. literalinclude:: ../scripts/initialize.py
    :caption: scripts/initialize.py

Initialize database
-------------------

.. autofunction:: calendar_bot.initDB.init_db
    :noindex:

.. autofunction:: calendar_bot.initDB.create_calendar_table
    :noindex:

.. autofunction:: calendar_bot.initDB.create_init_status_table
    :noindex:

.. autofunction:: calendar_bot.initDB.create_process_status_table
    :noindex:

Register bot
------------

.. autofunction:: calendar_bot.registerBot.init_bot
    :noindex:

.. autofunction:: calendar_bot.registerBot.register_bot
    :noindex:

.. autofunction:: calendar_bot.registerBot.register_bot_domain
    :noindex:

Run bot
=======

.. literalinclude:: ../main.py
    :caption: main.py

.. autofunction:: calendar_bot.calendar_bot.start_calendar_bot
    :noindex:

.. autofunction:: calendar_bot.router.getRouter
    :noindex:

.. autoclass:: calendar_bot.callbackHandler.CallbackHandler
    :members:
    :noindex:

.. autoclass:: calendar_bot.check_and_handle_actions.CheckAndHandleActions
    :members:
    :noindex:

util functions
--------------

.. autofunction:: calendar_bot.model.data.make_text
    :noindex:

.. autofunction:: calendar_bot.model.data.make_quick_reply
    :noindex:

.. autofunction:: calendar_bot.model.data.make_image_carousel
    :noindex:

.. autofunction:: calendar_bot.externals.send_message.push_message
    :noindex:




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
