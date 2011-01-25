#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from BeautifulSoup import BeautifulSoup as bs
import urllib2, sys, re, os, imp
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
    try:
        title = soup.head.title.contents[0].encode("utf-8")
    except:
        title = contents.head.title.contents
        
    return '<h1><a href="%s">%s</h1></a></h1>' % \
        (url, title) \
        + str(contents)


url = sys.argv[1]
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
f = opener.open(url)
soup = bs(f)

preprocessed = filter_soup(config.prefilter, url, soup)[1]

fmsg = format_html_message(url, config.postfilter, preprocessed)

msg = MIMEText(fmsg, "html")

msg['X-Entry-URL'] = url
msg['Subject'] = unicode(preprocessed.head.title.contents[0])
msg['From'] = config.mail_from
msg['To'] = config.mail_to

config.send_mail(config.mail_from, config.mail_to, msg)
