import json
from xml.sax import SAXParseException

import attr
from hyperlink import URL
from klein import Klein
from lxml import html
from lxml.builder import E
from lxml.etree import tostring
from treq.testing import StubTreq
from twisted.internet import defer
from twisted.trial.unittest import SynchronousTestCase

from feed_aggregation import FeedAggregation, FeedRetrieval
from feed_aggregation._service import Feed, Channel, Item, ResponseNotOk

FEEDS = (
    Feed(
        'http://feed-1.invalid/rss.xml',
        Channel(
            title='First feed',
            link='http://feed-1/',
            items=(Item(title='First item', link='#first'),)
        )
    ),
    Feed(
        'http://feed-2.invalid/rss.xml',
        Channel(
            title='Second feed',
            link='http://feed-2/',
            items=(Item(title='Second item', link='#second'),)
        )
    )
)


@attr.s
class StubFeed(object):
    _feeds = attr.ib()
    _app = Klein()

    def resource(self):
        return self._app.resource()

    @_app.route('/rss.xml')
    def return_xml(self, request):
        host = request.getHeader(b'host')
        try:
            return self._feeds[host]
        except KeyError:
            request.setResponseCode(404)
            return b'Unknown host: ' + host


def make_xml(feed):
    channel = feed._channel
    return tostring(
        E.rss(E.channel(
            E.title(channel.title),
            E.link(channel.link),
            *[E.item(E.title(item.title), E.link(item.link)) for item in channel.items],
            version=u'2.0'
        ))
    )


class TestFeedRetrieval(SynchronousTestCase):
    def setUp(self):
        service = StubFeed({URL.from_text(feed._source).host.encode('ascii'): make_xml(feed) for feed in FEEDS})
        treq = StubTreq(service.resource())
        self.retriever = FeedRetrieval(treq=treq)

    def assertTag(self, tag, name, attributes, text):
        self.assertEqual(tag.tagName, name)
        self.assertEqual(tag.attributes, attributes)
        self.assertEqual(tag.children, [text])

    def test_response_not_ok(self):
        no_feed = StubFeed({})
        retriever = FeedRetrieval(StubTreq(no_feed.resource()))
        failed_feed = self.successResultOf(retriever.retrieve('http://missing.invalid/rss.xml'))
        self.assertEqual(failed_feed.as_json(), {'error': 'Failed to load http://missing.invalid/rss.xml: 404'})
        self.assertTag(failed_feed.as_html(), 'a', {'href': 'http://missing.invalid/rss.xml'},
                       'Failed to load feed: 404')

    def test_unexpected_failure(self):
        empty = StubFeed({b'empty.invalid': b''})
        retriever = FeedRetrieval(StubTreq(empty.resource()))
        failed_feed = self.successResultOf(retriever.retrieve('http://empty.invalid/rss.xml'))
        msg = "SAXParseException('no element found')"
        self.assertEqual(failed_feed.as_json(), {'error': 'Failed to load http://empty.invalid/rss.xml: ' + msg})
        self.assertTag(failed_feed.as_html(), 'a', {'href': 'http://empty.invalid/rss.xml'},
                       'Failed to load feed: ' + msg)
        self.assertTrue(self.flushLoggedErrors(SAXParseException))

    def test_retrieve(self):
        for feed in FEEDS:
            parsed = self.successResultOf(self.retriever.retrieve(feed._source))
            self.assertEqual(parsed, feed)


class TestFeedAggregation(SynchronousTestCase):
    def setUp(self):
        self.client = StubTreq(FeedAggregation(FEEDS).resource())

    @defer.inlineCallbacks
    def get(self, url):
        response = yield self.client.get(url)
        self.assertEqual(response.code, 200)
        content = yield response.content()
        defer.returnValue(content)

    def test_render_HTML(self):
        content = self.successResultOf(self.get(u'http://test.invalid/'))
        parsed = html.fromstring(content)
        self.assertEqual(
            parsed.xpath(u'/html/body/div/table/tr/th/a/text()'),
            [u'First feed', u'Second feed']
        )
        self.assertEqual(
            parsed.xpath(u'/html/body/div/table/tr/th/a/@href'),
            [u'http://feed-1/', u'http://feed-2/']
        )
        self.assertEqual(
            parsed.xpath(u'/html/body/div/table/tr/td/a/text()'),
            [u'First item', u'Second item']
        )
        self.assertEqual(
            parsed.xpath(u'/html/body/div/table/tr/td/a/@href'),
            [u'#first', u'#second']
        )

    def test_render_JSON(self):
        content = self.successResultOf(
            self.get(u'http://test.invalud/?json=true'))
        parsed = json.loads(content)
        self.assertEqual(
            parsed,
            {
                u'feeds': [
                    {
                        u'title': u'First feed',
                        u'link': u'http://feed-1/',
                        u'items': [
                            {
                                u'title': u'First item',
                                u'link': u'#first'
                            }
                        ]
                    },
                    {
                        u'title': u'Second feed',
                        u'link': u'http://feed-2/',
                        u'items': [
                            {
                                u'title': u'Second item',
                                u'link': u'#second'
                            }
                        ]
                    }
                ]
            }
        )
