#!/usr/bin/env python3
#coding:utf8

"""
Author:       ottocho
Filename:     OINP-updates/mail.py
Date:         2019-03-07 10:18 PM
Description:  send mail via sendgrid
"""

import sendgrid
from sendgrid.helpers.mail import *

from config import *

def _send(subject, html, receivers):
    for email_recver in receivers:
        sg = sendgrid.SendGridAPIClient(apikey=SG_API_KEY)
        from_email = Email(EMAIL_SENDER)
        to_email = Email(email_recver)
        content = Content("text/html", html)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(email_recver)
        print(response.status_code)
        print(response.body)
        print(response.headers)

def send_msg(subject, html):
    return _send(subject, html, EMAIL_RECVERS)

def send_dev(subject, html):
    return _send(subject, html, EMAIL_DEVS)

if __name__ == '__main__':
    subject = 'UPDATE! Ontario Immigrant Nominee Program'
    html = '<p><strong>test mail</strong></p>'
    send_dev(subject, html)
