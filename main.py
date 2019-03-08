#!/usr/bin/env python3
#coding:utf8

"""
Author:       ottocho
Filename:     OINP-updates/main.py
Date:         2019-03-07 10:18 PM
Description:  fetch news and send email
"""

import os
import re
import json
import traceback
from datetime import datetime
from collections import defaultdict

import requests
from bs4 import BeautifulSoup

from mail import send_dev, send_msg
from config import *

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
    return (int(dm), int(dd), int(dy))

def fetch_news_tags():
    '''
    get the main part of the news website
    '''
    headers = {
        'User-Agent': HTTP_USER_AGENT,
        'Accept': '*/*',
        'Content-Encoding': 'gzip',
    }
    value = requests.get(URL_DATA_SOURCE, timeout=HTTP_TIMEOUT, headers=headers).json()
    html = value['body']['und'][0]['safe_value']
    soup = BeautifulSoup(html, 'html5lib')
    return soup.body.children

def parse_news_tags():
    '''
    parse the content lines
    '''
    # get content first
    tags = fetch_news_tags()

    started = False
    new_trunk = []
    trunks = defaultdict(list)
    last_date = None
    for tag in tags:
        if tag.name == 'h2' and tag.has_attr('id') and tag['id'].startswith('section-'):
            # the Month tag
            continue
        if tag.string:
            # remove blank line
            tag_string = re.sub(r'\s', '', tag.string)
            if not tag_string:
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
            idx = '%d-%02d-%02d-%02d' % (dy, dm, dd, (sl-idx))
            result.append((idx, news))
    return result

def get_last_update():
    if not os.path.isfile(PATH_LAST_UPDATE):
        return
    with open(PATH_LAST_UPDATE) as fobj:
        return json.loads(fobj.read())

def write_last_update(new_update):
    # update history data
    data = json.dumps(new_update, indent=4)
    with open(PATH_LAST_UPDATE, 'w') as fobj:
        fobj.write(data)
    with open(PATH_NEW_UPDATE, 'w') as fobj:
        fobj.write(data)

def main():
    print(datetime.now())

    # get new data from api
    new_update = parse_news_tags()
    # get last data from local cache data
    last_update = get_last_update()
    # write new data to local cache data
    write_last_update(new_update)

    if not last_update:
        print('initial')
        return

    # compare data
    keyset_new = set([_t[0] for _t in new_update])
    keyset_last = set([_t[0] for _t in last_update])
    keys_new = keyset_new - keyset_last

    # no update, return
    if not keys_new:
        print('no update')
        return

    # send notification!
    dict_new_update = dict(new_update)
    for kn in keys_new:
        print('update %s' % kn)
        nn = dict_new_update[kn]
        subject = 'UPDATE: Ontario Immigrant Nominee Program (%s)' % kn
        html = ''.join(nn)
        html = EMAIL_PREFIX + html
        send_msg(subject, html)

if __name__ == '__main__':
    try:
        main()

    except (IndexError, ConnectionResetError, requests.exceptions.Timeout, requests.exceptions.ContentDecodingError):
        print('time out')

        n = 1
        o = { 'n': n }
        # check time out time
        if os.path.isfile(PATH_TIMEOUT_REC):
            rb = open(PATH_TIMEOUT_REC, 'r+')
            o = json.loads(rb.read())
            n = o['n']
            rb.close()
        print('timeout #%d' % n)
        if n > HTTP_TIMEOUT_THRES:
            html = '<strong><pre>ERROR Timeout Detection</pre></strong>'
            html = EMAIL_PREFIX + html
            subject = 'ERROR: Ontario Immigrant Nominee Program'
            print(subject, html)
            send_dev(subject, html)
            n = 0

        # store timeout time
        wb = open(PATH_TIMEOUT_REC, 'w+')
        o['n'] = n + 1
        wb.write(json.dumps(o))
        wb.close()

    except Exception as e:
        exs = traceback.format_exc()
        html = '<strong><pre>%s</pre></strong>' % exs
        html = EMAIL_PREFIX + html
        subject = 'ERROR: Ontario Immigrant Nominee Program '
        print(subject, exs)
        send_dev(subject, html)
