import feedparser
import treq
from twisted.internet import defer
from twisted.internet import reactor as twisted_reactor
from twisted.web.template import tags, slot
from twisted.web import http
from klein import Klein, Plating


class SimpleFeedAggregation(object):
    application = Klein()
    common_page = Plating(
        tags=tags.html(
            tags.head(tags.title('Feed Aggregator 1.0')),
            tags.body(tags.div(slot(Plating.CONTENT))),
        )
    )

    def __init__(self, reactor, feed_urls):
        self._reactor = reactor
        self._feed_urls = feed_urls

    @defer.inlineCallbacks
    def retrieve_field(self, url):
        response = yield treq.get(url, timeout=30.0, reactor=self._reactor)
        if response.code != http.OK:
            fail_reason = http.RESPONSES[response.code]
            raise RuntimeError(f'Failed: {response.code} {fail_reason}')
        content = yield response.content()
        defer.returnValue(feedparser.parse(content))

    @common_page.routed(
        application.route('/'),
        tags.div(render='feeds:list')(slot('item'))
    )
    def feeds(self, request):
        def render_feed(feed):
            feed_title = feed[u'feed'][u'title']
            feed_link = feed[u'feed'][u'link']
            return tags.table(
                tags.tr(tags.th(tags.a(feed_title, href=feed_link)))
            )([
                tags.tr(tags.td(tags.a(entry[u'title'], href=entry[u'link'])))
                for entry in feed[u'entries']
            ])
        return {
            u'feeds': [
                self.retrieve_field(url).addCallback(render_feed)
                for url in self._feed_urls
            ]
        }


if __name__ == '__main__':
    web_service = SimpleFeedAggregation(twisted_reactor, [
        'http://feeds.bbci.co.uk/news/technology/rss.xml',
        'http://planet.twistedmatrix.com/rss20.xml',
    ])
    web_service.application.run('localhost', 8080)
