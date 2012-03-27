# -*- coding: utf-8 -*-
"""Tests for txStatHat"""

from __future__ import division, print_function, unicode_literals


from decimal import Decimal

import os

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

        def setUp(self):
            self.sh = txstathat.txStatHat(EZ_KEY)

        def _add_ok_check(self, deferred):
            """Add callback that checks whether the API returned a success."""
            deferred.addCallback(
                lambda s: self.assertEqual(s, b'{"status":200,"msg":"ok"}')
            )
            return deferred

        def test__whether_stathat_is_reachable(self):
            d = getPage(txstathat.API_URI)
            d.addCallback(lambda s: self.assertEqual(
                s, b'{"status":500,"msg":"no ezkey specified"}'))
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
