from pyramid import config, response


def hello_world(request):
    return response.Response('Hello World!')


if __name__ == '__main__':
    with config.Configurator() as conf:
        conf.add_route('hello', '/')
        conf.add_view(hello_world, route_name='hello')
        application = conf.make_wsgi_app()
