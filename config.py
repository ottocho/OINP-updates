#!/usr/bin/env python3
#coding:utf8

"""
Author:       ottocho
Filename:     OINP-updates/config.py
Date:         2019-03-07 10:18 PM
Description:

    configuration

"""

from datetime import datetime

YEAR = datetime.now().year

''' token for sendgrid '''
SG_API_KEY = ''

''' email settings '''
EMAIL_RECVERS = [
]
EMAIL_DEVS = [
]
EMAIL_SENDER = ''

''' data source URL '''
_HOST = 'api.ontario.ca'
_PATH = '/api/drupal/page%%2F%d-ontario-immigrant-nominee-program-updates' % YEAR
_GET_PARAMS = 'fields=nid,field_body_beta,body'
URL_DATA_SOURCE = 'https://%s/%s?%s' % (_HOST, _PATH, _GET_PARAMS)

''' URL posting OINP news '''
URL_NEWS = 'https://www.ontario.ca/page/%d-ontario-immigrant-nominee-program-updates' % YEAR
EMAIL_PREFIX = '<p><a target="_blank" href="%s">%s</a></p>' % (URL_NEWS, URL_NEWS)

''' path to file storing records '''
PATH_DB = 'db/'
PATH_LAST_UPDATE = PATH_DB + '/' + 'last.json'
PATH_NEW_UPDATE = PATH_DB + '/' + '%s.json' % datetime.now().strftime('%Y-%m%d-%H%M')
PATH_TIMEOUT_REC = PATH_DB + '/' + 'timeout.json'

''' http settings '''
HTTP_TIMEOUT = 15
HTTP_TIMEOUT_THRES = 500 # send email if timeout too much
HTTP_USER_AGENT = 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'

''' month to day number '''
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
