#!/usr/bin/env python3
#coding:utf8

"""
Author:       ottocho
Filename:     send_mail.py
Date:         2017-11-14 21:10
Description:

send mail via sendgrid

"""

import os

import sendgrid
from sendgrid.helpers.mail import *

SG_KEY_FILE = 'private/SG_API_KEY'
SENDER_FILE = 'private/SENDER'
RECVER_FILE = 'private/RECVER'
DEBUGGER_FILE = 'private/DEBUGGER'

def send_mail(subject, html):
    # get config
    apikey = open(SG_KEY_FILE).read().strip()
    sender_email = open(SENDER_FILE).read().strip()
    rs = [ i.strip() for i in open(RECVER_FILE).read().split() ]

    for recver_email in rs:
        # api send
        sg = sendgrid.SendGridAPIClient(apikey=apikey)
        from_email = Email(sender_email)
        to_email = Email(recver_email)
        content = Content("text/html", html)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(recver_email)
        print(response.status_code)
        print(response.body)
        print(response.headers)

def send_debug(subject, html):
    # get config
    apikey = open(SG_KEY_FILE).read().strip()
    sender_email = open(SENDER_FILE).read().strip()
    recver_email = open(DEBUGGER_FILE).read().strip()

    # api send
    sg = sendgrid.SendGridAPIClient(apikey=apikey)
    from_email = Email(sender_email)
    to_email = Email(recver_email)
    content = Content("text/html", html)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(recver_email)
    print(response.status_code)
    print(response.body)
    print(response.headers)

if __name__ == '__main__':
    subject = 'UPDATE! Ontario Immigrant Nominee Program'
    html = '<p><strong>test mail</strong></p>'
    send_debug(subject, html)
