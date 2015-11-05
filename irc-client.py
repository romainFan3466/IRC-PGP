#! /usr/bin/env python

# Romain F.

# Doc at : http://pythonhosted.org/irc/irc.html


import sys
import socket
import irc.client
import jaraco.logging



def listen_to(connection):
    soc = connection.socket
    buf = ''
    while connection.is_connected():
        buf += soc.recv(1024).decode("utf-8")
        print(buf)

def send_it(connection, target):
    while 1:
        line = sys.stdin.readline().strip()
        if not line:
            break
        connection.privmsg(target, line)
    connection.quit("Bye Bye")


def main():
    
    port = 6666
    nickname = "mybot"
    target = "#1"
    server = "127.0.0.1"

    reactor = irc.client.Reactor()
    try:
        c = reactor.server().connect(server, port, nickname)
        c.join(target)


        # Uncomment/comment the two following lines to switch the server listener/sender

        #listen_to(c)
        send_it(c, target)


    except irc.client.ServerConnectionError:
        print(sys.exc_info()[1])
        raise SystemExit(1)

    reactor.process_forever()

if __name__ == '__main__':
    main()