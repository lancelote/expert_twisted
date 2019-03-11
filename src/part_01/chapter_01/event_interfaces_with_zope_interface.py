from twisted.internet.interfaces import IReactorTime
from twisted.internet.task import Clock
from twisted.internet import reactor
from zope.interface import providedBy
from zope.interface.verify import verifyObject

clock = Clock()

assert list(providedBy(clock)) == [IReactorTime]
assert verifyObject(IReactorTime, clock)
assert verifyObject(IReactorTime, reactor)
