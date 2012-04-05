# -*- coding: utf-8 -*-
"""Tests for txStatHat"""

from __future__ import division, print_function, unicode_literals


from decimal import Decimal

import os

from twisted.internet import defer
from twisted.trial import unittest
from twisted.web.client import getPage

import txstathat


EZ_KEY = os.environ.get('TEST_EZ_KEY')


if EZ_KEY:
    class RemoteTestCase(unittest.TestCase):
        """Test by actually accessing StatHat.

        Reads the StatHat key from the environment variable called TEST_EZ_KEY.
        Uses stats called *txSHTestCall*, *txSHTestCount* and *txSHTestValue*.
        This test case is skipped if no key is defined.

        Unfortunately, as StatHat isn't really real time, we have to eyeball
        the results in the web interface.

        """

        TEST_COUNT = b'txSHTestCount'
        TEST_VALUE = b'txSHTestValue'
        TEST_CALL = b'txSHTestCall'

        MSG_OK = b'{"status":200,"msg":"ok"}'
        MSG_NO_EZKEY = b'{"status":500,"msg":"no ezkey specified"}'

        def setUp(self):
            self.sh = txstathat.txStatHat(EZ_KEY)
            # some tests tinker with the API URI
            self.old_API_URI = txstathat.API_URI

        def tearDown(self):
            txstathat.API_URI = self.old_API_URI

        def _add_ok_check(self, deferred):
            """Add callback that checks whether the API returned a success."""
            deferred.addCallback(
                lambda s: self.assertEqual(s, self.MSG_OK)
            )
            return deferred

        def test__whether_stathat_is_reachable(self):
            d = getPage(txstathat.API_URI)
            d.addCallback(lambda s: self.assertEqual(s, self.MSG_NO_EZKEY))
            return d

        def test_ssl_detection(self):
            pred = self.assertTrue if txstathat.have_ssl else self.assertFalse
            pred(txstathat.API_URI.startswith('https'))

        def test_make_call(self):
            d = self.sh._make_call({'stat': self.TEST_CALL, 'value': 25.3})
            return self._add_ok_check(d)

        def test_count_by_implicit_one(self):
            d = self.sh.count(self.TEST_COUNT)
            return self._add_ok_check(d)

        def test_count_by_explicit_argument(self):
            d = self.sh.count(self.TEST_COUNT, 42)
            return self._add_ok_check(d)

        def test_value_float(self):
            d = self.sh.value(self.TEST_VALUE, 0.42)
            return self._add_ok_check(d)

        def test_value_decimal(self):
            d = self.sh.value(self.TEST_VALUE, Decimal('0.42'))
            return self._add_ok_check(d)

        def test_ignore_errors_really_ignores(self):
            d1 = txstathat.txStatHat(b'').count(self.TEST_COUNT, 42)
            d1.addCallback(lambda s: self.assertEqual(s, self.MSG_NO_EZKEY))

            txstathat.API_URI = b'http://invalid.invalid'
            d2 = self.sh.count(b'does not matter')
            d2.addCallback(lambda rv: self.assertIsNone(rv))

            return defer.DeferredList([d1, d2])

        def test_check_api_result(self):
            d = txstathat.txStatHat(b'', ignore_errors=False) \
                    .count(self.TEST_COUNT, 42)
            return self.assertFailure(d, txstathat.txStatHatApiException)
