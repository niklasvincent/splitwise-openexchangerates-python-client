splitwise-openexchangerates-python-client
=========================================

This package provides integration with `Splitwise <https://splitwise.com/>`_, an expense sharing platform.

It seamlessly converts the `Splitwise <https://splitwise.com/>`_ expenses to a common currently (GBP by default) using `Open Exchange Rates <https://openexchangerates.org/>`_.

Example Usage
-------------

Install using PIP:

.. code:: python

    pip install git+https://github.com/nlindblad/splitwise-openexchangerates-python-client.git


.. code:: python

    from splitwise.openexchangerate import OpenExchangeRatesClient
    from splitwise.client import Splitwise

    splitwise = Splitwise(
                   "API_BASE_URL",
                   "CONSUMER_KEY",
                   "CONSUMER_SECRET",
                   "OAUTH_TOKEN_KEY",
                   "OAUTH_TOKEN_SECRET",
                   OpenExchangeRatesClient("OPEN_EXCHANGE_RATES_API_KEY")
    )

    expenses = splitwise.get_expenses()
