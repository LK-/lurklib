#    This file is part of Lurklib.
#    Copyright (C) 2011  LK-
#
#    Lurklib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Lurklib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Lurklib.  If not, see <http://www.gnu.org/licenses/>.

""" High level abstraction Lurklib file. """

from __future__ import with_statement
from . import core

__version__ = '1.0.1'


class Client(core._Core):
    """ High level IRC abstraction class """
    def process_once(self, timeout=0.01):
        """
        Handles an event and calls it's handler
        Optional arguments:
        * timeout=0.01 - Wait for an event until the timeout is reached.
        """
        try:
            event = self.recv(timeout)
            if event:
                event_t = event[0]
                event_c = event[1]

                if event_t == 'JOIN':
                    self.on_join(event_c[0], event_c[1])
                elif event_t == 'PART':
                    self.on_part(event_c[0], event_c[1], event_c[2])
                elif event_t == 'PRIVMSG':
                    if event_c[1] in self.channels.keys():
                        self.on_chanmsg(event_c[0], event_c[1], event_c[2])
                    else:
                        self.on_privmsg(event_c[0], event_c[2])
                elif event_t == 'NOTICE':
                    if event_c[1] in self.channels.keys():
                        self.on_channotice(event_c[0], event_c[1], event_c[2])
                    else:
                        self.on_privnotice(event_c[0], event_c[2])
                elif event_t == 'CTCP':
                    if event_c[1] in self.channels.keys():
                        self.on_chanctcp(event_c[0], event_c[1], event_c[2])
                    else:
                        self.on_privctcp(event_c[0], event_c[2])
                elif event_t == 'CTCP_REPLY':
                    self.on_ctcp_reply(event_c[0], event_c[2])
                elif event_t == 'MODE':
                    if event_c[0] == self.current_nick:
                        self.on_umode(event_c[1])
                    else:
                        self.on_cmode(event_c[0], event_c[1], event_c[2])
                elif event_t == 'KICK':
                    self.on_kick(event_c[0], event_c[1], event_c[2], \
                    event_c[3])
                elif event_t == 'INVITE':
                    self.on_invite(event_c[0], event_c[2])
                elif event_t == 'NICK':
                    self.on_nick(event_c[0], event_c[1])
                elif event_t == 'TOPIC':
                    self.on_topic(event_c[0], event_c[1], event_c[2])
                elif event_t == 'QUIT':
                    self.on_quit(event_c[0], event_c[1])
                elif event_t == 'LUSERS':
                    self.on_lusers(event_c)
                elif event_t == 'ERROR':
                    self.on_error(event_c[0])
                elif event_t == 'UNKNOWN':
                    self.on_unknown(event_c[0])

        except self.LurklibError as exception:
            self.on_exception(exception)

    def mainloop(self):
        """
        Handles events and calls their handler for infinity.
        """
        while self.keep_going:
            with self.lock:
                if self.on_connect and not self.readable(2):
                    self.on_connect()
                    self.on_connect = None
                if not self.keep_going:
                    break
                self.process_once()

    def on_connect(self):
        pass

    def on_join(self, from_, channel):
        pass

    def on_part(self, from_, channel, reason):
        pass

    def on_chanmsg(self, from_, channel, message):
        pass

    def on_privmsg(self, from_, message):
        pass

    def on_channotice(self, from_, channel, notice):
        pass

    def on_privnotice(self, from_, notice):
        pass

    def on_chanctcp(self, from_, channel, message):
        pass

    def on_privctcp(self, from_, message):
        pass

    def on_ctcp_reply(self, from_, message):
        pass

    def on_cmode(self, from_, channel, mode):
        pass

    def on_umode(self, mode):
        pass

    def on_kick(self, from_, channel, who, reason):
        pass

    def on_invite(self, from_, channel):
        pass

    def on_nick(self, from_, new_nick):
        pass

    def on_topic(self, from_, channel, new_topic):
        pass

    def on_quit(self, from_, reason):
        pass

    def on_lusers(self, data):
        pass

    def on_error(self, message):
        pass

    def on_unknown(self, message):
        pass

    def on_exception(self, exception):
        pass
