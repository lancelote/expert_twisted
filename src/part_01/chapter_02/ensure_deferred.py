from twisted.internet.defer import ensureDeferred, Deferred


async def async_increment(d):
    x = await d
    return x + 1


awaited = Deferred()
add_deferred = ensureDeferred(async_increment(awaited))
add_deferred.addCallback(print)
awaited.callback(1)


# Exception propagation
async def async_add(d):
    x = await d
    return x + 1


awaited = Deferred()
add_deferred = ensureDeferred(async_add(awaited))
add_deferred.addCallback(print)
awaited.callback(None)
