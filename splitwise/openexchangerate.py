from collections import defaultdict, namedtuple
from datetime import date, timedelta
import hashlib
import json
import os
import time
import urllib
import urllib2
import urlparse


class OpenExchangeRatesClient(object):

    def __init__(self, token, baseUrl = "https://openexchangerates.org/api", cacheDirectory = "/tmp"):
        self.token = token
        self.baseUrl = baseUrl
        self.cacheDirectory = cacheDirectory

    def _cacheFile(self, url):
        """Construct cache filename for request"""
        m = hashlib.md5()
        m.update(url)
        key = m.hexdigest()
        return os.path.join(self.cacheDirectory, key)

    def _fromCache(self, url):
        """Load cached response from file"""
        try:
            with open(self._cacheFile(url), 'r') as f:
                return f.read()
        except:
            return None

    def _toCache(self, content, url):
        """Save cached response to file"""
        try:
            with open(self._cacheFile(url), 'w') as f:
                f.write(content)
                return True
        except Exception as e:
            print "Could not write cache entry for %s: %s" % (url, e)
            return False

    def _fromApi(self, url):
        """Retrieve from API"""
        req = urllib2.Request(url = url)
        f = urllib2.urlopen(req)
        return f.read()

    def _conversionsForDate(self, date):
        """Retrieve currency conversions for date"""
        queryUrl = self.baseUrl + "/historical/%s.json?app_id=%s" % (time.strftime("%Y-%m-%d", date), self.token)
        content = self._fromCache(queryUrl)
        if not content:
            content = self._fromApi(queryUrl)
            self._toCache(content, queryUrl)
        return json.loads(content)

    def convert(self, amount, fromCurrency, toCurrency, date):
        """Convert from one currency to the other, at a specific point in time, if necessary"""
        if fromCurrency == toCurrency:
            return amount
        data = self._conversionsForDate(date)
        exchangeRate = float(data.get("rates").get(fromCurrency)) / float(data.get("rates").get(toCurrency))
        return round(amount/exchangeRate, 2)
