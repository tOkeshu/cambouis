from socket import socket, AF_INET, SOCK_STREAM
from cambouis.utils import throttle

class IRC(object):

    def __init__(self, host, port=6667, nick=None, realname=None):
        self.host = host
        self.port = port
        self.nick = nick # TODO: raise if nick is None
        self.realname = realname or nick
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.buffer = ''

    def connect(self):
        self.socket.connect((self.host, self.port))
        self.socket.send("NICK %s\r\n" % self.nick)
        self.socket.send("USER %s %s bla :%s\r\n" % (self.nick, self.host, self.realname))

    def stream(self):
        self.buffer += self.socket.recv(1024)
        while True:
            pivot = self.buffer.find('\r\n')
            while pivot >= 0:

                if pivot >= 0:
                    data, self.buffer = (self.buffer[:pivot],
                                         self.buffer[pivot + 2:])
                    yield Event(data)
                pivot = self.buffer.find('\r\n')
            self.buffer += self.socket.recv(1024)

    def ping(self, data):
        self.socket.send('PONG %s\r\n' % data)

    @throttle(5, 1)
    def privmsg(self, recipient, data):
        data = data.replace('\n', ' ')
        self.socket.send('PRIVMSG %s :%s\r\n' % (recipient, data))

    def close(self):
        self.socket.close()


class Event(object):

    def __init__(self, data):
        """Breaks a message from an IRC server into its prefix, command, and arguments.
        """
        prefix = ''
        trailing = []
        self.data = data

        if not data:
           raise IRCBadMessage("Empty line.")
        if data[0] == ':':
            prefix, data = data[1:].split(' ', 1)
        if data.find(' :') != -1:
            data, trailing = data.split(' :', 1)
            args = data.split()
            args.append(trailing)
        else:
            args = data.split()
        command = args.pop(0)

        self.prefix, self.command, self.args = prefix, command, args
        self.type = self.command

        self.nick = None
        self.where = None
        self.msg = None

        if self.type == 'PRIVMSG':
            self.nick = self.prefix.split('!', 1)[0]
            self.where = self.args[0]
            self.msg = self.args[1]
        if self.type == 'PING':
            self.msg = ''.join(self.args)

    def __str__(self):
        return '<Event %s>' % repr((self.prefix, self.command, self.args))

