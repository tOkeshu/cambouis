from cambouis.irc import IRC
from cambouis.twitter import firehose
from spool import coroutine, select

CHANNEL = '#channel'

@coroutine
def irc(irc):
    chan = coroutine.self()
    for event in irc.stream():
        chan.put(event)

@coroutine
def twitter():
    chan = coroutine.self()
    for tweet in firehose():
        chan.put(tweet)

class Bot(object):

    def __init__(self, **kwargs):
        self.config = kwargs
        self.irc = IRC(**kwargs['irc'])
        self.streams = []
        self.commands = [('!len ', self.len)]

    def run(self):
        self.irc.connect()

        i, t = self.streams = [irc(self.irc), twitter()]
        for source in select(*self.streams):
            if source is i:
                self.on_irc(i.get())
            if source is t:
                self.on_twitter(t.get())

    def on_irc(self, event):
        print(event)
        if event.type == 'PING':
            self.irc.ping(event.msg)
        if event.type == 'PRIVMSG':
            self.dispatch(event)
        elif event.type == 'ERROR':
            self.stop()

    def on_twitter(self, tweet):
        message = "%s: %s %s" % (tweet.user, tweet.status, tweet.permalink)
        print(message)
        self.irc.privmsg(CHANNEL, message.encode('utf-8'))

    def dispatch(self, event):
        for prefix, method in self.commands:
            if event.msg.startswith(prefix):
                method(event, event.msg[len(prefix):])

    def len(self, event, message):
        self.irc.reply(event, str(len(message)))

    def stop(self):
        for stream in self.streams:
            stream.close()
        self.irc.close()

