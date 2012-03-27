# -*- coding: utf-8 -*-
"""StatHat bindings"""

from __future__ import division, print_function, unicode_literals


import urllib

from twisted.web.client import getPage


try:
    from OpenSSL import SSL  # noqa
    have_ssl = True
except:
    have_ssl = False

API_URI = b'http{}://api.stathat.com/ez'.format(b's' if have_ssl else b'')


class txStatHat(object):

    """An API wrapper for StatHat.com."""

    def __init__(self, ezkey):
        """Initialize a txStatHat instance.

        Does no network activity.

        :param ezkey: your API key, i.e. your e-mail address by default.

        """

        self.default_args = {'ezkey': ezkey}

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
        return d

    def count(self, stat, count=1):
        """Add *count* to *stat*.

        :param stat: a StatHat counter stat
        :param count: the value to add to the counter. 1 by default.
        :type count: integer
        :rtype: twisted.internet.defer.Deferred

        """

        return self._make_call({'stat': stat, 'count': unicode(count)})

    def value(self, stat, value):
        """Submit *value* to *stat*.

        :param stat: a StatHat value stat
        :param value: the value to submit
        :type value: float or decimal.Decimal
        :rtype: twisted.internet.defer.Deferred

        """

        return self._make_call({'stat': stat, 'value': unicode(value)})
