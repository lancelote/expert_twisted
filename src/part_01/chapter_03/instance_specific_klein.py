import klein
from twisted.internet import task
from twisted.internet import reactor


class SlowIncrementWebServer(object):
    application = klein.Klein()

    def __init__(self, reactor):
        self._reactor = reactor

    @application.route('/<int:amount>')
    def slow_increment(self, request, amount):
        new_amount = amount + 1
        message = f'Hello! Your new amount is: {new_amount}'
        return task.deferLater(self._reactor, 1.0, str.encode, message, 'ascii')


if __name__ == '__main__':
    web_service = SlowIncrementWebServer(reactor)
    web_service.application.run('localhost', 8080)
