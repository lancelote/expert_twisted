from wsgiref import simple_server

from src.part_02.chapter_05 import wsgi_hello

simple_server.make_server('127.0.0.1', 8000, wsgi_hello.application).serve_forever()
