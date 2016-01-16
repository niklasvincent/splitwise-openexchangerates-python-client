from collections import defaultdict, namedtuple
from datetime import date, timedelta
import hashlib
import json
import os
import time
import urllib
import urllib2
import urlparse

from model import Category, Expense


class Splitwise(object):

    def __init__(self, base_url, consumer_key, consumer_secret, oauth_token_key, oauth_token_secret, currencyConversionClient, defaultCurrency = "GBP"):
        global oauth
        import oauth2 as oauth
        self.base_url = base_url
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.oauth_token_key = oauth_token_key
        self.oauth_token_secret = oauth_token_secret
        self.defaultCurrency = defaultCurrency
        self.currencyConversionClient = currencyConversionClient

        self.currencyConversions = defaultdict()

        self._setupClient()

    def _setupClient(self):
        """Construct OAuth client for Splitwise"""
        consumer = oauth.Consumer(self.consumer_key, self.consumer_secret)
        token = oauth.Token(self.oauth_token_key, self.oauth_token_secret)

        self.client = oauth.Client(consumer, token)

    def request(self, url, method = "GET"):
        """Make HTTP request and deserialise the JSON response"""
        resp, content = self.client.request(url, method)
        return json.loads(content)

    def build_url(self, path, query = dict()):
        """Build a full URL using the relative URL"""
        query_string = urllib.urlencode(query) if query else ""
        return "%s/%s?%s" % (self.base_url, path, query_string)

    def get_expenses(self):
        """Get all expenses"""
        expenses = []
        to_date = lambda x: time.strptime(x[0:10], "%Y-%m-%d")
        week_nbr = lambda x: date(x.tm_year, x.tm_mon, x.tm_mday).isocalendar()[1]
        categories = self.get_categories()
        user_id = self.get_current_user_id()
        for e in self.request(self.build_url("get_expenses", {"limit" : "0"})).get("expenses"):
            try:
                if e.get("deleted_by") or e.get("creation_method") in ["debt_consolidation", "payment"]:
                    continue
                expense_date = to_date(e.get("date"))
                user_share = self.calculate_currency_conversion(
                    self.get_user_share(e, user_id),
                    e.get("currency_code"),
                    self.defaultCurrency,
                    expense_date
                    )
                if user_share <= 0:
                    continue
                expense = Expense(
                    e.get("id"),
                    user_id,
                    expense_date.tm_year,
                    expense_date.tm_mon,
                    expense_date.tm_mday,
                    week_nbr(expense_date),
                    e.get("description"),
                    categories.get(e.get("category").get("id")),
                    user_share
                )
                expenses.append(expense)
            except Exception as exp:
                print exp
                continue
        return expenses

    def get_categories(self):
        """Get all categories"""
        categories = {}
        for subcategories in self.request(self.build_url("get_categories", {})).get("categories"):
            subcategories = subcategories.get("subcategories")
            for subcategory in subcategories:
                category = Category(
                    subcategory.get("id"),
                    subcategory.get("name"),
                    subcategory.get("icon").split("/")[-2:][0].capitalize()
                )
                categories[subcategory.get("id")] = category
        return categories

    def get_current_user_id(self):
        """Get the ID of the currently authenticated user"""
        return self.request(self.build_url("get_current_user", {})).get("user").get("id")

    def get_user_share(self, expense, user_id):
        """Get the proportional share for the user ID as part of this expense"""
        return float([user["owed_share"] for user in expense["users"] if user["user"]["id"] == user_id][0])

    def calculate_currency_conversion(self, amount, fromCurrency, toCurrency, expenseDate):
        """Convert from one currency to the other, at a specific point in time, if necessary"""
        return self.currencyConversionClient.convert(amount, fromCurrency, toCurrency, expenseDate)
