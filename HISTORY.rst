.. :changelog:

History
-------

0.2.0 (2012-04-??)
++++++++++++++++++

* txStatHat now ignores errors by default in order to minimize disruption and
  boilerplate code due to possible StatHat outages.
* On the other hand, if one checks for errors, txStatHat also checks the return
  value of the API and throws a txStatHatApiException on errors.
