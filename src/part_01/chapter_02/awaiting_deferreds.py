import operator

from twisted.internet.defer import Deferred


async def await_future_like(obj):
    result = await obj
    print(result)


deferred = Deferred()
coroutine = await_future_like(deferred)
assert coroutine.send(None) is deferred
deferred.callback('the result')
try:
    coroutine.send(None)
except StopIteration:
    pass


# awaiting a Deferred resolves to whatever the Deferred does after its normal
# callback and errback
d = Deferred()
d.addCallback(print, 'was received by a callback')
d.addCallback(operator.add, 2)


async def await_deferred():
    await d


g = await_deferred()
g.send(None)
d.callback(1)
