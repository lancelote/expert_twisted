def failing_generator():
    try:
        yield
    except ValueError:
        print('caught ValueError inside')


traceback_gen = failing_generator()
next(traceback_gen)

try:
    # continue generator raising an exception inside
    traceback_gen.throw(TypeError)
except TypeError:
    print('TypeError was caught in the global scope')

catching_gen = failing_generator()
next(catching_gen)

try:
    catching_gen.throw(ValueError)
except StopIteration:
    print('generator is empty')
