from twisted.internet.defer import Deferred

outer_deferred = Deferred()


def print_and_pass_through(result, *args):
    print('print_and_pass_through', ' '.join(args), 'received', result)
    return result


outer_deferred.addCallback(print_and_pass_through, '1')

inner_deferred = Deferred()
inner_deferred.addCallback(print_and_pass_through, '2', 'a')
inner_deferred.addCallback(print_and_pass_through, '2', 'b')


def return_inner_deferred(result, number):
    print('return_inner_deferred', number, 'received', result)
    print('returning inner_deferred...')
    return inner_deferred


# Callback loop inside outer_deferred will detect Deferred return type of the next callback pausing execution util
# inner_deferred resolves to a value
outer_deferred.addCallback(return_inner_deferred, '2')

outer_deferred.addCallback(print_and_pass_through, '3')
outer_deferred.addCallback(print_and_pass_through, '4')

outer_deferred.callback('result')
inner_deferred.callback('result')
