# -*- coding: utf-8 -*-
"""StatHat bindings for Twisted"""

from __future__ import division, print_function, unicode_literals


import json
import urllib

from twisted.web.client import getPage


try:
    from OpenSSL import SSL  # noqa
    have_ssl = True
except:
    have_ssl = False

API_URI = b'http{}://api.stathat.com/ez'.format(b's' if have_ssl else b'')


class txStatHatApiException(Exception):

    """Raised whenever the API returns anything else than a 200.

    Extends the base Exception class by a status field, the error message of
    the API is used as the Exception message.

    """

    def __str__(self):
        return b'status={0.status}, msg="{0.message}"'.format(self)

    def __init__(self, status, msg):
        self.status = status
        Exception.__init__(self, msg)


class txStatHat(object):

    """An API wrapper for StatHat.com’s EZ API."""

    def __init__(self, ezkey, ignore_errors=True):
        """Initialize a txStatHat instance.

        Does no network activity.

        One usually doesn’t want an outage at StatHat break your application.
        Therefore, errors while submitting stats are blissfully ignored by
        default.

        :param ezkey: your API key, i.e. your e-mail address by default.
        :param ignore_errors: indicator whether errors should be ignored.

        """

        self.default_args = {'ezkey': ezkey}
        self.ignore_errors = ignore_errors

    def _make_call(self, args):
        """Build postdata using ezkey and supplied dict *args* and post it."""
        post_dict = self.default_args.copy()
        post_dict.update(args)
        d = getPage(
                API_URI,
                method=b'POST',
                postdata=urllib.urlencode(post_dict),
                headers={
                    b'Content-Type': b'application/x-www-form-urlencoded'
                    },
                )

        if self.ignore_errors:
            d.addErrback(self._swallow_errors)
        else:
            d.addCallback(self._check_api_result)

        return d

    def _swallow_errors(self, failure):
        """Swallow and ignore any exception."""

    def _check_api_result(self, result):
        """Check whether the API call was successful."""
        try:
            res = json.loads(result)
            status = res['status']
            msg = res['msg']
        except:
            raise txStatHatApiException(
                    500,
                    b'Could not parse result: "{}"'.format(result))
        if status != 200:
            raise txStatHatApiException(status, msg)

    def count(self, stat, count=1):
        """Add *count* to *stat*.

        :param stat: a StatHat counter stat
        :param count: the value to add to the counter. 1 by default.
        :type count: integer
        :rtype: twisted.internet.defer.Deferred
        :raises txstathat.txStatHatApiException: If ignore_errors is False and
            StatHat doesn’t return a 200.
        :raises Twisted’s network related exceptions: If ignore_errors is False
            Twisted’s network exceptions are let through.

        """

        return self._make_call({'stat': stat, 'count': unicode(count)})

    def value(self, stat, value):
        """Submit *value* to *stat*.

        Raises the same exceptions as :py:func:txStatHat.count().

        :param stat: a StatHat value stat
        :param value: the value to submit
        :type value: float or decimal.Decimal
        :rtype: twisted.internet.defer.Deferred

        """

        return self._make_call({'stat': stat, 'value': unicode(value)})
