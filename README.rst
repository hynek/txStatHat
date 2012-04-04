txStatHat
=========

A Twisted_ API wrapper for StatHat_’s `EZ API`_.

The usage is as simple as::

    from twisted.internet import reactor
    from twisted.internet.defer import inlineCallbacks
    from txstathat import txStatHat


    @inlineCallbacks
    def doSomeStats():
        sh = txStatHat('keyOrEmail', ignore_errors=True)
        yield sh.count('aCounter')  # Counts by 1 by default
        yield sh.count('anotherCounter', 42)
        yield sh.value('aValue', 0.42)


    reactor.callLater(1, doSomeStats)
    reactor.run()

By default, errors are swallowed silently so disruptions at StatHat don’t lead
to disruption in your services by accident. To get network exceptions as well
as API error messages, set ``ignore_errors=False`` when instantiating txStatHat.

Depending on the availability of pyOpenSSL_, txStatHat uses HTTPS for API
calls if possible.

.. _Twisted: http://twistedmatrix.com/
.. _StatHat: http://www.stathat.com/
.. _`EZ API`: http://www.stathat.com/docs/api
.. _pyOpenSSL: http://pypi.python.org/pypi/pyOpenSSL/
