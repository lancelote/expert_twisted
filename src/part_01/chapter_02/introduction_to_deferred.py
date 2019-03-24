from twisted.internet.defer import Deferred, AlreadyCalledError

d = Deferred()


def cb_print(result, *args, **kwargs):
    print('result = ', result)
    print('args =', args)
    print('kwargs =', kwargs)


assert d.addCallback(cb_print, 'positional', keyword=1) is d
d.callback('result')

# Deferred can't be called back second time
try:
    d.callback('wops')
except AlreadyCalledError as e:
    print('AlreadyCalledError was raised trying to call back second time')

# Calling back before adding the callback function
d2 = Deferred()
d2.callback('the result')
d2.addCallback(print)
