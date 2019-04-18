import klein


application = klein.Klein()


@application.route('/<int:amount>')
def hello(request, amount):
    new_amount = amount + 1
    message = f'Hello! Your new amount is: {new_amount}'
    return message.encode('ascii')


if __name__ == '__main__':
    application.run('localhost', 8080)
