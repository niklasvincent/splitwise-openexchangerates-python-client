from collections import defaultdict, namedtuple
from datetime import date, timedelta
import hashlib
import json
import os
import time
import urllib
import urllib2
import urlparse


class Fixer(object):

    def __init__(self, baseUrl = "http://api.fixer.io/", cacheDirectory = "/tmp"):
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
        try:
            req = urllib2.Request(url = url)
            f = urllib2.urlopen(req)
            return f.read()
        except Exception as e:
            print "Could not get exchange rate: %s, %s" % (url, e)

    def _conversionsForDate(self, date):
        """Retrieve currency conversions for date"""
        queryUrl = self.baseUrl + "/%s" % (time.strftime("%Y-%m-%d", date))
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
        exchangeRate = float(data['rates'][fromCurrency]) / float(data['rates'][toCurrency])
        return round(amount/exchangeRate, 2)
