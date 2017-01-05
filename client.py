#!/usr/bin/env python2

import connection
import readline
import threading
import time

server = None

class UpdateLoop(threading.Thread):
    def run(self):
        while True:
            if server is not None:
                msg = server.fetch_messages()
                dms = server.fetch_direct()

                for dm in dms:
                    dm["nick"] = "DIRECT: " + dm["nick"]

                msg += dms

                msg = sorted(msg, key = lambda k: k["timestamp"])

                for m in msg:
                    disp = "[" + str(m["timestamp"]) + "] " + m["nick"] + "#" + m["id"] + ": " + m["body"]
                    print disp

def login(cmd):
    global server

    server = connection.Connection(cmd[0], cmd[1])

    print "Login succesful!"

commands = {
        "/login" : login
        }

def main():
    loop = UpdateLoop()
    loop.daemon = True
    loop.start()
    
    while True:
        msg = raw_input()

        if msg.startswith("/"):
            cmd = msg.split(" ")
            
            if cmd[0] in commands:
                commands[ cmd[0] ](cmd[1:])

            else:
                print "Command not recognized."

            continue

        if server is None:
            print "You have to connect to a server to talk."
            continue

        server.send_message(msg)

main()
