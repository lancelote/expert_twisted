from twisted.internet import task
from twisted.internet import reactor
import klein

application = klein.Klein()


@application.route('/<int:amount>')
def slow_increment(request, amount):
    new_amount = amount + 1
    message = f'Hello! Your new amount is: {new_amount}'
    return task.deferLater(reactor, 1.0, str.encode, message, 'ascii')


if __name__ == '__main__':
    application.run('localhost', 8080)
