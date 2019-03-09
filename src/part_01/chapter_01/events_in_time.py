from twisted.internet import reactor

call = reactor.callLater(1.5, print, 'hello from the past')
# The call can be canceled preventing the output
# call.cancel()
reactor.run()
