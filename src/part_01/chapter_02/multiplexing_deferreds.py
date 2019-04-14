from twisted.internet.defer import Deferred, DeferredList, gatherResults

url1 = Deferred()
url2 = Deferred()
url_list = DeferredList([url1, url2])
url_list.addCallback(print)
url2.callback('url2')
url1.callback('url1')

# Causing one deferred in deferred list to fail
succeeds = Deferred()
fails = Deferred()
list_of_deferreds = DeferredList([succeeds, fails])
list_of_deferreds.addCallback(print)
fails.errback(Exception())
succeeds.callback('OK')

# fireOnOneCallback example
no_value = Deferred()
gets_value = Deferred()
waits_for_one = DeferredList([no_value, gets_value], fireOnOneCallback=True)
waits_for_one.addCallback(print)
gets_value.callback('the value')


# Get the faster deferred example
def faster_of_two(d1, d2):
    def extract_value(value_and_index):
        value, index = value_and_index
        return value
    url_list = DeferredList(
        [d1, d2],
        fireOnOneCallback=True,
        fireOnOneErrback=True
    )
    return url_list.addCallback(extract_value)


# Gathering results
d1, d2 = Deferred(), Deferred()
results = gatherResults([d1, d2])
results.addCallback(print)
d1.callback(1)
d2.callback(2)

d1, d2 = Deferred(), Deferred()
fails = gatherResults([d1, d2])
fails.addErrback(print)
d1.errback(Exception())
