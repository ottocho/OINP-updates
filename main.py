#!/usr/bin/env python3
#coding:utf8

"""
Author:       ottocho
Filename:     fetch_update.py
Date:         2017-11-14 21:10
Description:

    HTTP request and split out the part of the lastest update of ONIP
    send email if new ONIP update

"""

import os
import re
import json
import traceback
import datetime
from collections import defaultdict

import requests
from bs4 import BeautifulSoup

from send_mail import send_mail, send_debug

''' dir to store data '''
DIR = 'db/'

''' target '''
URL = 'http://www.ontarioimmigration.ca/en/pnp/OI_PNPNEW.html'
EMAIL_PREFIX = '<p><a target="_blank" href="%s">%s</a></p>' % (URL, URL)


''' http timeout '''
TIMEOUT = 15
TIMEOUT_THRES = 500 # send email if timeout too much
TIMEOUT_REC = DIR + '/' + 'timeout.json'

''' history data '''
LAST_JS = DIR + '/' + 'last.json'
M2D = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Sept": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


''' user agent to pretend normal user '''
UA = 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'

def try_release_line(l):
    '''
    each news MAY be started with a line with date underlined.
    use this line to be the starter of one news

    indicated line:
    '<p><strong><span style=" text-decoration: underline;">December 6th, 2018</span></strong></p>'
    '''
    PTN = r'''
    style="[ ]+text-decoration[ ]*:[ ]*underline.+>                 # prefix
    (?P<month>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec
              |January|February|March|April|May|June|July|August
              |September|October|November|December)\.?[ ]+          # month
    (?P<day>[0-9]+)(?:st|nd|rd|th|ST|ND|RD|TH)?,?[ ]+               # day
    (?P<year>20[21][67890])                                         # year
    '''
    rk = re.compile(PTN, re.VERBOSE)
    t = rk.findall(l)
    return t

def get_main_part():
    '''
    get the main part of the news website and return the list of `h1` and `p`(content)
    '''
    headers = {
        'User-Agent': UA,
        'Accept': '*/*',
        'Content-Encoding': 'gzip',
    }
    html = requests.get(URL, timeout=TIMEOUT, headers=headers).content
    soup = BeautifulSoup(html, 'html5lib')

    main_div = soup.find_all(class_="main_content")[0]
    lines = main_div.find_all(("h1", "p", "ul"))
    return lines

def parse():
    '''
    parse the content lines
    '''
    # get content first
    lines = get_main_part()

    start_tag = False
    # end_tag = False
    new_trunk = []
    trunks = defaultdict(list)
    news_date = None
    for line in lines:
        l = str(line)
        chk = try_release_line(l)
        if chk :
            if start_tag:
                # this new tag is: 1 begining of new one 2 the one after end of old trunk
                # end_tag = True
                trunks[news_date].append(new_trunk)
            news_date = chk[0]
            # begin a new trunk
            start_tag = True
            # end_tag = False
            new_trunk = [l]
        else:
            # not a new start, just append
            new_trunk.append(l)

    result = []
    # make lines a plain list and give them index
    for date, newslist in trunks.items():
        _dm, dd, dy = date
        dm = M2D[_dm]
        sl = len(newslist)
        for idx, news in enumerate(newslist):
            idx = '%d-%02d-%02d-%02d' % (int(dy), int(dm), int(dd), (sl-idx))
            result.append((idx, news))
    return result

def get_last_updates():
    if not os.path.isfile(LAST_JS):
        return None
    with open(LAST_JS) as fobj:
        return json.loads(fobj.read())

def main():
    ts = datetime.datetime.now().strftime('%Y-%m%d-%H%M')
    print('')
    print(ts)

    # get new data
    new_updates = parse()
    # get last data
    last_updates = get_last_updates()

    # update history data
    js = json.dumps(new_updates, indent=5)
    with open(LAST_JS, 'w') as fobj:
        fobj.write(js)
    with open('%s/%s.json' % (DIR, ts), 'w') as fobj:
        fobj.write(js)

    if not last_updates:
        print('initial')
        return

    # compare data
    keyset_new = set([_t[0] for _t in new_updates])
    keyset_last = set([_t[0] for _t in last_updates])
    keys_new = keyset_new - keyset_last

    # no update, return
    if not keys_new:
        print('no update')
        return

    # send mail !!
    for kn in keys_new:
        print('update %s' % kn)
        nn = dict(new_updates)[kn]
        subject = 'UPDATE: Ontario Immigrant Nominee Program (%s)' % kn
        html = ''.join(nn)
        html = EMAIL_PREFIX + html
        send_mail(subject, html)

if __name__ == '__main__':
    try:
        main()

    except (IndexError, ConnectionResetError, requests.exceptions.Timeout, requests.exceptions.ContentDecodingError):
        print('time out')

        n = 1
        o = { 'n': n }
        # check time out time
        if os.path.isfile(TIMEOUT_REC):
            rb = open(TIMEOUT_REC, 'r+')
            o = json.loads(rb.read())
            n = o['n']
            rb.close()
        print('timeout #%d' % n)
        if n > TIMEOUT_THRES:
            html = '<strong><pre>timeout %d > %d</pre></strong>' % (n, TIMEOUT_THRES)
            html = EMAIL_PREFIX + html
            subject = 'ERROR: Ontario Immigrant Nominee Program '
            print(subject, html)
            send_debug(subject, html)
            n = 0

        # store timeout time
        wb = open(TIMEOUT_REC, 'w+')
        o['n'] = n + 1
        wb.write(json.dumps(o))
        wb.close()

    except Exception as e:
        exs = traceback.format_exc()
        html = '<strong><pre>%s</pre></strong>' % exs
        html = EMAIL_PREFIX + html
        subject = 'ERROR: Ontario Immigrant Nominee Program '
        print(subject, exs)
        send_debug(subject, html)
