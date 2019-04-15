from twisted.internet import defer
from twisted.trial import unittest


def faster_of_two(d1, d2):
    def extract_value(value_and_index):
        value, index = value_and_index
        return value
    url_list = defer.DeferredList(
        [d1, d2],
        fireOnOneCallback=True,
        fireOnOneErrback=True
    )
    return url_list.addCallback(extract_value)


class TestFastestOfTwo(unittest.SynchronousTestCase):
    def test_no_result(self):
        d1 = defer.Deferred()
        self.assertNoResult(d1)
        d2 = defer.Deferred()
        self.assertNoResult(d2)
        self.assertNoResult(faster_of_two(d1, d2))

    def test_result_is_first_deferreds_result(self):
        gets_result_first = defer.Deferred()
        newer_gets_result = defer.Deferred()
        fastest_deferreds = faster_of_two(gets_result_first, newer_gets_result)
        self.assertNoResult(fastest_deferreds)
        result = 'the result'
        gets_result_first.callback(result)
        actual_result = self.successResultOf(fastest_deferreds)
        self.assertIs(result, actual_result)

    def test_fired_deferred_is_first_result(self):
        result = 'the result'
        fastest_deferred = faster_of_two(defer.Deferred(),
                                         defer.succeed(result))
        actual_result = self.successResultOf(fastest_deferred)
        self.assertIs(result, actual_result)

    def test_both_deferreds_fired(self):
        first = 'first'
        second = 'second'
        fastest_deferred = faster_of_two(defer.succeed(first),
                                         defer.succeed('second'))
        actual_result = self.successResultOf(fastest_deferred)
        self.assertIs(first, actual_result)

    def test_fail_deferred(self):
        class ExceptionType(Exception):
            pass

        fastest_deferred = faster_of_two(defer.fail(ExceptionType()),
                                         defer.Deferred())
        failure = self.failureResultOf(fastest_deferred)
        failure.trap(defer.FirstError)
        failure.value.subFailure.trap(ExceptionType)
