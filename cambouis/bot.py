from cambouis.irc import IRC

class Bot(object):

    def __init__(self, **kwargs):
        self.config = kwargs
        self.irc = IRC(**kwargs['irc'])

    def run(self):
        self.irc.connect()
        for event in self.irc.stream():
            if event.type == 'PING':
                self.irc.ping(event.msg)
            if event.type == 'PRIVMSG':
                self.irc.privmsg(event.nick, event.msg)
            elif event.type == 'ERROR':
                self.stop()

            print('<= %s' % event.data)

    def stop(self):
        self.irc.close()

