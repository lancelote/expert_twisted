import types


async def function():
    pass


print(function())

# Can't be interated over
try:
    list(function())
except TypeError:
    pass

# Has send and throw methods
try:
    function().send(None)
except StopIteration:
    pass
try:
    function().throw(ValueError)
except ValueError:
    pass


# Can await other coroutines
async def returns_value(value):
    return 1


async def awaits_coroutine(c):
    value = await c
    print(value)


try:
    awaits_coroutine(returns_value(1).send(None))
except StopIteration:
    pass


# Can't await plain generator
def plain_generator():
    yield 1


async def broken_coroutine_awaits_generator():
    await plain_generator()


try:
    broken_coroutine_awaits_generator().send(None)
except TypeError:
    pass


# The chain of the generators
def g1():
    yield from g2()


def g2():
    yield from g3()


def g3():
    yield from g4()


def g4():
    yield from g5()


def g5():
    yield 1


print(next(g1()))


# yield from requires an iterable object to advance generator
def yield_to_iterable(source):
    print('Yielding from object of type', type(source))
    yield from source


print(list(yield_to_iterable(range(3))))


# Make generator awaitable
@types.coroutine
def make_base():
    return (yield 'hello from a base object')


async def awaits_base(base):
    value = await base
    print('from awaits_base:', value)


awaiter = awaits_base(make_base())
print(awaiter.send(None))
try:
    awaiter.send('the result')
except StopIteration:
    pass


# Futures-like objects from asyncio
class FutureLike:
    _MISSING = 'MISSING'

    def __init__(self):
        self.result = self._MISSING

    def __next__(self):
        if self.result is self._MISSING:
            return self
        raise StopIteration(self.result)

    def __iter__(self):
        return self

    def __await__(self):
        return iter(self)


async def await_future_like(obj):
    result = await obj
    print(result)


obj = FutureLike()
coroutine = await_future_like(obj)
assert coroutine.send(None) is obj
obj.result = 'the result'
try:
    coroutine.send(None)
except StopIteration:
    pass
