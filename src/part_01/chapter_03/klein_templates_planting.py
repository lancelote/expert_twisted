from twisted.internet import task, reactor
from twisted.web.template import tags, slot
from klein import Klein, Plating


class SlowIncrementWebService(object):
    application = Klein()
    common_page = Plating(
        tags=tags.html(
            tags.head(
                tags.title(slot('title')),
                tags.style('#amount { font-weight: bold; }'
                           '#message { font-style: italic; }')
            ),
            tags.body(
                tags.div(slot(Plating.CONTENT))
            )
        )
    )

    def __init__(self, reactor):
        self._reactor = reactor

    @common_page.routed(
        application.route('/<int:amount>'),
        tags.div(
            tags.span('Hello! Your new amount is: ', id='message'),
            tags.span(slot('new_amount'), id='amount'),
        )
    )
    def slow_increment(self, request, amount):
        slots = {
            'title': 'Slow Increment',
            'new_amount': amount + 1,
        }
        return task.deferLater(self._reactor, 1.0, lambda: slots)


if __name__ == '__main__':
    web_service = SlowIncrementWebService(reactor)
    web_service.application.run('localhost', 8080)
