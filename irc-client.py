#! /usr/bin/env python

# Romain F.

# Doc at : http://pythonhosted.org/irc/irc.html


import sys
import socket
import irc.client
import jaraco.logging
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--mode",
        help="Set the bot mode : listener or sender. Default is listener",
        default="listener"
    )
    parser.add_argument(
        "-ho",
        "--host",
        help="IRC Server host. Default is Romain's server host",
        default="51.255.38.201"
    )
    parser.add_argument(
        "-ch",
        "--channel",
        help="IRC Server channel to join. Need to start by # "
    )
    parser.add_argument(
        "-nick",
        "--nickname",
        help="Client nickname"
    )
    parser.add_argument(
        "-po",
        "--port",
        help="IRC Server port. Default is 6666",
        type=int,
        default=6666
    )
    parser.add_argument(
        "-pw",
        "--password",
        help="IRC Server password if required"
    )

    return parser.parse_args()

def listen_to(connection):
    soc = connection.socket
    buf = ''
    while connection.is_connected():
        buf = soc.recv(1024).decode("utf-8")
        print(buf)

def send_it(connection, target):
    while 1:
        line = sys.stdin.readline().strip()
        if not line:
            break
        connection.privmsg(target, line)
    connection.quit("Bye Bye")


def main():

    args = parse_args()
    port = args.port
    nickname = args.nickname
    target = args.channel
    server = args.host
    password = None if not args.password else args.password


    reactor = irc.client.Reactor()
    try:
        c = reactor.server().connect(server, port, nickname,password=password)
        c.join(target)

        if args.mode == "listener":
            listen_to(c)
        elif args.mode == "sender":
            send_it(c, target)
        else:
            print("no mode specified")
            raise SystemExit(1)

    except irc.client.ServerConnectionError:
        print(sys.exc_info()[1])
        raise SystemExit(1)

    reactor.process_forever()

if __name__ == '__main__':
    main()
