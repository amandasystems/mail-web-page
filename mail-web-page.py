#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup as bs
import urllib, sys, re, os, ConfigParser, imp
from email.mime.text import MIMEText

# init conf object

config = imp.load_source("config", os.path.expanduser('~/.mail-web-page-config.py'))

def filter_soup(rules, url, soup):
    for rule in rules:
        if re.match(rule[0], url):
            #print "Rule %s matches" % rule[0]
            return (True, rule[1](url, soup))
    return (False, soup) # no rule matched: return input data and a flag telling so.

def format_html_message(url, rules, soup):
    contents = filter_soup(rules, url, soup)[1]
    return '<h1><a href="%s">%s</h1></a></h1>' % \
        (url, soup.head.title.contents[0].encode("utf-8")) \
        + contents.prettify()


url = sys.argv[1]
f = urllib.urlopen(url)
soup = bs(f)

preprocessed = filter_soup(config.prefilter, url, soup)[1]

msg = MIMEText(format_html_message(url, config.postfilter, preprocessed), "html")

msg['X-Entry-URL'] = url
msg['Subject'] = preprocessed.head.title.contents[0].encode("utf-8")
msg['From'] = config.mail_from
msg['To'] = config.mail_to

config.send_mail(config.mail_from, config.mail_to, msg)
