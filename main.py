#!/usr/bin/env python3
#coding:utf8

"""
Author:       ottocho
Filename:     OINP-updates/main.py
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

YEAR = datetime.datetime.now().year

NEW_URL = 'https://www.ontario.ca/page/%d-ontario-immigrant-nominee-program-updates' % YEAR
EMAIL_PREFIX = '<p><a target="_blank" href="%s">%s</a></p>' % (URL, URL)

''' dir to store data '''
DIR = 'db/'
''' history data '''
LAST_JS = DIR + '/' + 'last.json'

''' data source URL '''
_HOST = 'api.ontario.ca'
_PATH = '/api/drupal/page%%2F%d-ontario-immigrant-nominee-program-updates' % YEAR
_GET_PARAMS = 'fields=nid,field_body_beta,body'
DATA_SOURCE_URL = 'https://%s/%s?%s' % (_HOST, _PATH, _GET_PARAMS)

''' http timeout '''
TIMEOUT = 15
TIMEOUT_THRES = 500 # send email if timeout too much
TIMEOUT_REC = DIR + '/' + 'timeout.json'

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

def parse_date_title(l):
    '''
    use this line to be the starter of one news
    indicated line: `December 6th, 2018`
    '''
    if not l:
        return l
    PTN = r'''
    (?P<month>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec
              |January|February|March|April|May|June|July|August
              |September|October|November|December)\.?[ ]+          # month
    (?P<day>[0-9]+)(?:st|nd|rd|th|ST|ND|RD|TH)?[ ]*,?[ ]*           # day
    (?P<year>20[21][67890])                                         # year
    '''
    rk = re.compile(PTN, re.VERBOSE)
    t = rk.findall(l)
    if len(t) == 0:
        return
    _dm, dd, dy = t[0]
    dm = M2D[_dm]
    return (dm, dd, dy)

''' user agent to pretend normal user '''
USER_AGENT = 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'

def get_main_part():
    '''
    get the main part of the news website
    '''
    # FIXME testing
    '''
    with open('./jj.json') as fobj:
        value = json.loads(fobj.read())
        content = value['body']['und'][0]['safe_value']
        soup = BeautifulSoup(content, 'html5lib')
        return soup.body.children
    '''

    headers = {
        'User-Agent': USER_AGENT,
        'Accept': '*/*',
        'Content-Encoding': 'gzip',
    }
    html = requests.get(DATA_SOURCE_URL, timeout=TIMEOUT, headers=headers).content
    soup = BeautifulSoup(html, 'html5lib')
    return soup.body.children

def parse():
    '''
    parse the content lines
    '''
    # get content first
    tags = get_main_part()

    started = False
    new_trunk = []
    trunks = defaultdict(list)
    last_date = None
    for tag in tags:
        if tag.name == 'h2' and tag.has_attr('id') and tag['id'].startswith('section-'):
            # the Month tag
            continue
        if tag.string and set([ c for c in tag.string ]) == {'\n'}:
            # blank line
            continue
        if tag.name == 'h3':
            new_date = parse_date_title(tag.string)
            if new_date: # begining of a new message
                if started:
                    trunks[last_date].append(new_trunk)
                started = True
                last_date = new_date
                new_trunk = [ str(tag) ]
                continue
        new_trunk.append(str(tag))

    result = []
    # make lines a plain list and give them index
    for date, newslist in trunks.items():
        dm, dd, dy = date
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
