#!/usr/bin/env python2

import rest

class Connection(object):
    def __init__(self, server, nick, token = None):
        self.lastsync = 0
        self.dmsync = 0

        self.server = server
        self.nick = nick
        self.token = token

        self.api = rest.RestfulAPI("http://" + server + ":8080")

        self.login()

    def login(self):
        if self.token is None:
            code, user = self.api.login(nick = self.nick)
            
            self.token = user["token"]
        else:
            code, user = self.api.user(token = self.token)

        self.nick = user["nick"]
        self.id = user["id"]

    def fetch_messages(self, time = None):
        if time is None:
            msg = self.api.update[self.lastsync]()[1]
            
            if len(msg) > 0:
                self.lastsync = msg[0]["timestamp"]
            return msg
        return self.api.update[time]()[1]

    def fetch_direct(self, time = None):
        if time is None:
            msg = self.api.direct(token = self.token, timestamp = self.dmsync)[1]
            
            if len(msg) > 0:
                self.dmsync = msg[0]["timestamp"]
            return msg
        return self.api.direct(token = self.token, timestamp = time)[1]

    def send_message(self, content):
        self.api.send(token = self.token, body = content)

    def send_direct(self, to, content):
        self.api.direct[to](token = self.token, body = content)

    def lookup_user(self, nick):
        code, users = self.api.users(nick = nick)
        
        ids = [user["id"] for user in users]
        return ids

    def change_nick(self, nick):
        code, user = self.api.profile(token = self.token, nick = nick)

        return user
