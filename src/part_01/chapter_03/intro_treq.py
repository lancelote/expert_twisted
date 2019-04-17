from __future__ import print_function
from argparse import ArgumentParser

import feedparser
from twisted.internet import defer, task
from twisted.web import http
import treq


@task.react  # Will start and stop a reactor
@defer.inlineCallbacks
def download(reactor):
    parser = ArgumentParser()
    parser.add_argument('url')
    arguments = parser.parse_args()
    response = yield treq.get(arguments.url, timeout=30.0, reactor=reactor)
    if response.code != http.OK:
        reason = http.RESPONSES[response.code]
        raise RuntimeError(f'Failed: {response.code} {reason}')
    content = yield response.content()
    parsed = feedparser.parse(content)
    print(parsed['feed']['title'])
    print(parsed['feed']['description'])
    print('*** ENTRIES ***')
    for entry in parsed['entries']:
        print(entry['title'])


# Run against https://planet.twistedmatrix.com/rss20.xml for example
