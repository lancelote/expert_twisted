from functools import partial

import attr
import treq
import feedparser
from klein import Klein, Plating
from twisted.web.template import tags as t, slot
from twisted.logger import Logger


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


@attr.s(frozen=True)
class FailedFeed(object):
    _source = attr.ib()
    _reason = attr.ib()

    def as_json(self):
        return {'error': 'Failed to load {}: {}'.format(self._source, self._reason)}

    def as_html(self):
        return t.a(href=self._source)('Failed to load feed: {}'.format(self._reason))


class ResponseNotOk(Exception):
    """A response returned a non-200 status code."""


@attr.s
class FeedAggregation(object):
    _retrieve = attr.ib()
    _urls = attr.ib()
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
        def convert(feed):
            return feed.as_json() if request.args.get(b'json') else feed.as_html()
        return {'feeds': [self._retrieve(url).addCallback(convert) for url in self._urls]}


@attr.s
class FeedRetrieval(object):
    _treq = attr.ib()
    _logger = Logger()

    def retrieve(self, url):
        self._logger.info('Downloading feed {url}', url=url)
        feed_deferred = self._treq.get(url)

        def check_code(response):
            if response.code != 200:
                raise ResponseNotOk(response.code)
            return response

        feed_deferred.addCallback(check_code)
        feed_deferred.addCallback(treq.content)
        feed_deferred.addCallback(feedparser.parse)

        def to_feed(parsed):
            if parsed[u'bozo']:
                raise parsed[u'bozo_exception']
            feed = parsed[u'feed']
            entries = parsed[u'entries']
            channel = Channel(feed[u'title'], feed[u'link'], tuple(Item(e[u'title'], e[u'link']) for e in entries))
            return Feed(url, channel)

        feed_deferred.addCallback(to_feed)

        def failed_feed_when_not_ok(reason):
            reason.trap(ResponseNotOk)
            self._logger.error('Could not download feed {url}: {code}', url=url, code=str(reason.value))
            return FailedFeed(url, str(reason.value))

        def failed_feed_on_unknown(failure):
            self._logger.failure('Unexpected {failure} downloading {url}', failure=failure, url=url)
            return FailedFeed(url, repr(failure.value))

        feed_deferred.addErrback(failed_feed_when_not_ok)
        feed_deferred.addErrback(failed_feed_on_unknown)

        return feed_deferred
