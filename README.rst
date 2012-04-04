txStatHat
=========

A Twisted_ API wrapper for StatHat_’s `EZ API`_.

The usage is as simple as::

    from twisted.internet import reactor
    from twisted.internet.defer import inlineCallbacks
    from txstathat import txStatHat


    @inlineCallbacks
    def doSomeStats():
        sh = txStatHat('ezKeyOrEmail')
        yield sh.count('aCounter')  # Counts by 1 by default
        yield sh.count('anotherCounter', 42)
        yield sh.value('aValue', 0.42)


    reactor.callLater(1, doSomeStats)
    reactor.run()

The ``ezKeyOrEmail`` is your e-mail address in the beginning, but can be
changed in the account settings to something more safe. There is no such thing
as a password.

By default, errors are swallowed silently so disruptions at StatHat don’t lead
to disruption in your services by accident. To get network exceptions as well
as API error messages, set ``ignore_errors=False`` when instantiating
txStatHat. You should only do so if you have really good reasons.

    **Please note**: At the moment, StatHat.com does *not* report an error when
    an incorrect EZ API key is submitted. Therefore the above example will work
    without any effect even if you don’t replace the API key.

StatHat.com seems to have generally a similar attitude towards errors as
txStatHat. They return an OK except if you use the API incorrectly (don’t
supply an API key for example). The difference is that if ``ignore_errors`` is
left at the default ``True``, network problems accessing the API are ignored as
well.

Depending on the availability of pyOpenSSL_, txStatHat uses HTTPS for API calls
if possible. While there isn’t much real damage an attacker can do to you if
(s)he hijacks your API key, I strongly suggest to install and use it.

.. _Twisted: http://twistedmatrix.com/
.. _StatHat: http://www.stathat.com/
.. _`EZ API`: http://www.stathat.com/docs/api
.. _pyOpenSSL: http://pypi.python.org/pypi/pyOpenSSL/
