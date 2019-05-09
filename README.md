# expert_twisted

Code from "[Expert Twisted][1]: Event-Driven and Asynchronous Programming with
Python" book by Mark Williams and contributors

## TOC

- [x] [Part 1: Foundation](src/part_01)
    - [x] [Chapter 1: An Introduction to Event-Driven Programming with Twisted](src/part_01/chapter_01)
        - [Basic Event Driven Program](src/part_01/chapter_01/basic_event_driven_program.py)
        - [Program with Multiple Events](src/part_01/chapter_01/program_with_multiple_events.py)
        - [`select` and Sockets](src/part_01/chapter_01/select_and_sockets.py)
        - [Event Loop around `select`](src/part_01/chapter_01/event_loop_around_select.py)
        - [Non-blocking Socket](src/part_01/chapter_01/non_blocking_socket.py)
        - [Custom Write Buffer](src/part_01/chapter_01/custom_write_buffer.py)
        - [Reactor with Transport](src/part_01/chapter_01/reactor_with_transport.py)
        - [Bytes Transport](src/part_01/chapter_01/bytes_transport.py)
        - [Event Driven Twisted Program](src/part_01/chapter_01/event_driven_twisted_program.py)
        - [Events in Time](src/part_01/chapter_01/events_in_time.py)
        - [Repeated Events with Looping Call](src/part_01/chapter_01/repeated_events_with_looping_call.py)
        - [Event Interfaces with `zope.interface`](src/part_01/chapter_01/event_interfaces_with_zope_interface.py)
        - [Flow Control with Producers and Consumers](src/part_01/chapter_01/flow_control_with_producers_and_consumers.py)
    - [x] [Chapter 2: An Introduction to Asynchronous Programming with Twisted](src/part_01/chapter_02)
        - [Introduction to Twisted Deferred](src/part_01/chapter_02/introduction_to_deferred.py)
        - [Errbacks and Failures](src/part_01/chapter_02/errbacks_and_failures.py)
        - [Composing Deferreds](src/part_01/chapter_02/composing_deferreds.py)
        - [Generator Throw](src/part_01/chapter_02/generator_throw.py)
        - [Coroutines with `yield from`](src/part_01/chapter_02/coroutines_with_yield_from.py)
        - [Coroutines Async and Await](src/part_01/chapter_02/coroutines_async_and_await.py)
        - [Awaiting Deferreds](src/part_01/chapter_02/awaiting_deferreds.py)
        - [Coroutines to Deferred with ensureDeferred](src/part_01/chapter_02/ensure_deferred.py)
        - [Multiplexing Deferreds](src/part_01/chapter_02/multiplexing_deferreds.py)
        - [Testing Deferreds](src/part_01/chapter_02/testing_deferreds.py)
    - [x] Chapter 3: Applications with treq and Klein
       - [Introducing `treq`](src/part_01/chapter_03/intro_treq.py)
       - [Introducing Klein](src/part_01/chapter_03/intro_klein.py)
       - [Klein and Deferreds](src/part_01/chapter_03/klein_and_deferreds.py)
       - [Instance-specific Klein Applications](src/part_01/chapter_03/instance_specific_klein.py)
       - [Klein Templates with Planting](src/part_01/chapter_03/klein_templates_planting.py)
       - [First Feed Aggregation Draft](src/part_01/chapter_03/feed_aggregation_first_draft.py)
       - [Feed Aggregation Project](src/part_01/chapter_03/feed_aggregation_project)
- [ ] Part 2: Projects
    - [x] [Chapter 4: Twisted in Docker](src/part_02/chapter_04)
        - [Building Python from Scratch](src/part_02/chapter_04/building_python_from_scratch/Dockerfile)
        - [Using Virtualenv inside Docker](src/part_02/chapter_04/using_virtualenv/Dockerfile)
        - [Using Pex inside Docker](src/part_02/chapter_04/using_pex/Dockerfile)
        - [Using NColony](src/part_02/chapter_04/using_ncolony/Dockerfile)
    - [ ] Chapter 5: Using Twisted as a WSGI Server
        - [Raw WSGI Application](src/part_02/chapter_05/wsgi_hello.py)
    - [ ] Chapter 6: Tahoe-LAFS: The Least-Authority File System
    - [ ] Chapter 7: Magic Wormhole
    - [ ] Chapter 8: Push Data to Browsers and Micro-services with WebSocket
    - [ ] Chapter 9: Applications with asyncio and Twisted
    - [ ] Chapter 10: Buildbot and Twisted
    - [ ] Chapter 11: Twisted and HTTP/2
    - [ ] Chapter 12: Twisted and Django Channels

[1]: https://www.goodreads.com/book/show/40167833-expert-twisted