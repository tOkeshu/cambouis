from datetime import datetime, timedelta

def throttle(hit_limit, time_limit):
    class Context(object):

        def __init__(self):
            self.counter = 0
            self.hit_limit = hit_limit
            self.time_limit = time_limit
            self.last = datetime.now()

    def _throttle(fun):
        ctx = Context()

        def _fun(*args):
            if ctx.counter >= ctx.hit_limit and \
                    (datetime.now() - ctx.last) > timedelta(0, time_limit, 0):
                ctx.last = datetime.now()
                ctx.counter = 0
            elif ctx.counter < ctx.hit_limit:
                ctx.counter += 1
                return fun(*args)
        return _fun
    return _throttle

