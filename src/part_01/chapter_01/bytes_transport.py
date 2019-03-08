import io


class BytesTransport(object):

    def __init__(self, protocol):
        self.protocol = protocol
        self.output = io.BytesIO()

    def write(self, data):
        self.output.write(data)

    def lose_connection(self):
        self.output.close()
        self.protocol.connection_lost(None)
