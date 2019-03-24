from twisted.internet.defer import Deferred
from twisted.python.failure import Failure

d3 = Deferred()


def cb_will_fail(number):
    print(1 / number)


d3.addCallback(cb_will_fail)
d3.addErrback(print)
d3.callback(0)

# Failure example
try:
    1 / 0
except ZeroDivisionError:
    f = Failure()  # absorb an active exception and its traceback
    print(f)
    print(f.check(ValueError))
    print(f.check(ValueError, ZeroDivisionError))

# Trapping the error
d4 = Deferred()


def eb_value_error(failure):
    failure.trap(ValueError)  # re-raise if doesn't match
    print('failure was ValueError')


def eb_type_error_and_zero_division_error(failure):
    exception_type = failure.trap(TypeError, ZeroDivisionError)
    print('failure was', exception_type)


d4.addCallback(cb_will_fail)
d4.addErrback(eb_value_error)
d4.addErrback(eb_type_error_and_zero_division_error)
d4.callback(0)

# Calling errback
d5 = Deferred()
d5.addErrback(print)

try:
    1 / 0
except ZeroDivisionError:
    d5.errback()
