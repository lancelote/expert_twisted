import attr
import treq
import feedparser
from klein import Klein, Plating
from twisted.web.template import tags as t, slot


@attr.s(frozen=True)
class Channel(object):
    title = attr.ib()
    link = attr.ib()
    items = attr.ib()


@attr.s(frozen=True)
class Item(object):
    title = attr.ib()
    link = attr.ib()


@attr.s(frozen=True)
class Feed(object):
    _source = attr.ib()
    _channel = attr.ib()

    def as_json(self):
        return attr.asdict(self._channel)

    def as_html(self):
        header = t.th(t.a(href=self._channel.link)(self._channel.title))
        return t.table(t.tr(header))(
            [t.tr(t.td(t.a(href=item.link)(item.title)))
             for item in self._channel.items]
        )


@attr.s
class FeedAggregation(object):
    _feeds = attr.ib()
    _app = Klein()
    _planting = Plating(
        tags=t.html(
            t.head(t.title('Feed Aggregator 2.0')),
            t.body(slot(Plating.CONTENT))
        )
    )

    def resource(self):
        return self._app.resource()

    @_planting.routed(
        _app.route('/'),
        t.div(render='feeds:list')(slot('item')),
    )
    def root(self, request):
        json_requested = request.args.get(b'json')

        def convert(feed):
            return feed.as_json() if json_requested else feed.as_html()

        return {'feeds': [convert(feed) for feed in self._feeds]}


@attr.s
class FeedRetrieval(object):
    _treq = attr.ib()

    def retrieve(self, url):
        feed_deferred = self._treq.get(url)
        feed_deferred.addCallback(treq.content)
        feed_deferred.addCallback(feedparser.parse)

        def to_feed(parsed):
            feed = parsed[u'feed']
            entries = parsed[u'entries']
            channel = Channel(feed[u'title'], feed[u'link'], tuple(Item(e[u'title'], e[u'link']) for e in entries))
            return Feed(url, channel)

        feed_deferred.addCallback(to_feed)
        return feed_deferred
