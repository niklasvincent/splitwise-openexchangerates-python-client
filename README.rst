# splitwise-openexchangerates-python-client

This package provides integration with [Splitwise](https://splitwise.com/), an expense sharing platform.

It seamlessly converts the [Splitwise](https://splitwise.com/) expenses to a common currently (GBP by default) using [Open Exchange Rates](https://openexchangerates.org/).

## Example Usage

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
