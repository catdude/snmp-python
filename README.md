# snmp-python
Python implementation of an SNMP polling engine

This needs to be a very quick engine, as it will be polling a LOT of
OIDs from a LOT of devices, pretty often, and stuffing the results
into an influxdb engine. It has not yet been determined whether
this engine will do the database writes, or will pass the data to
a message queue or some other distinct database-handling mechanism.

