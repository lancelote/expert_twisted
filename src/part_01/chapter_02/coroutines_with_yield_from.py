def e():
    print('begin e')
    a = yield 1
    return a + 2


def f():
    print('begin f')
    c = yield from e()
    print(c)


g = f()
print('send None')
print(g.send(None))
try:
    print('send 2')
    g.send(2)
except StopIteration:
    pass
