txStatHat
=========

A Twisted_ API wrapper for StatHat_.

The usage is as simple as::

    from twisted.internet import reactor
    from twisted.internet.defer import inlineCallbacks
    from txstathat import txStatHat


    @inlineCallbacks
    def doSomeStats():
        sh = txStatHat('keyOrEmail')
        yield sh.count('aCounter')  # Counts by 1 by default
        yield sh.count('anotherCounter', 42)
        yield sh.value('aValue', 0.42)


    reactor.callLater(1, doSomeStats)
    reactor.run()

Depending on the availability of pyOpenSSL, txStatHat uses https for API calls
if possible.

.. _Twisted: http://twistedmatrix.com/
.. _StatHat: http://www.stathat.com/
