#!/usr/bin/env python

from smtpd import SMTPServer
from imaplib import IMAP4, IMAP4_SSL, Time2Internaldate
from time import time
import email

import asyncore

config = {
    'smtpd_conf':{
        'smtpd_hostname':'127.0.0.1',
        'smtpd_port':'1026',
        },
    'imap4_conf':{
        'imap4_hostname':'imap.gmail.com',
        'imap4_port':'993',
        'imap4_mailbox':'Drafts',
        'imap4_ssl':'True',
        'imap4_login':'@gmail.com',
        'imap4_password':'',
        }
    }

class FakeSmtp(SMTPServer):
    def create_imap_connection_and_append(self, msg):
        if config['imap4_conf']['imap4_ssl'] == 'True':
            try:
                self.imap_server = IMAP4_SSL(config['imap4_conf']['imap4_hostname'],\
                        str(config['imap4_conf']['imap4_port']))
                self.imap_server.login(config['imap4_conf']['imap4_login'],\
                        config['imap4_conf']['imap4_password'])
                self.imap_server.select(config['imap4_conf']['imap4_mailbox'])
                self.imap_server.append(config['imap4_conf']['imap4_mailbox'],\
                        '',\
                        Time2Internaldate(time()),\
                        str(email.message_from_string(msg)))
                self.imap_server.close()
            except Exception, e:
                print 'Can not create connection with ssl: %s' % e
        elif config['imap4_conf']['imap4_ssl'] == 'False' or '':
            try:
                self.imap_server = IMAP4(config['imap4_conf']['imap4_hostname'],\
                        (config['imap4_conf']['imap4_port']))
                self.imap_server.login(config['imap4_conf']['imap4_login'],\
                        config['imap4_conf']['imap4_password'])
                self.imap_server.select(config['imap4_conf']['imap4_mailbox'])
                self.imap_server.append(config['imap4_conf']['imap4_mailbox'],\
                        '',\
                        Time2Internaldate(time()),\
                        str(email.message_from_string(msg)))
                self.imap_server.close()
            except Exception, e:
                print 'Can not create connection without ssl: %s' % e

    def process_message(self, peer, mailfrom, rcpttos, data):
        try:
            self.create_imap_connection_and_append(data)
        except Exception, e:
            print "Incoming message is not well formed. %s\n" % e
        return

def run():
    print "Start server:"
    try:
        server = FakeSmtp((config['smtpd_conf']['smtpd_hostname'], \
                int(config['smtpd_conf']['smtpd_port'])), None)
        print 'Server started'
        asyncore.loop()
    except KeyboardInterrupt:
        server.close()
if __name__ == '__main__':
    run()
