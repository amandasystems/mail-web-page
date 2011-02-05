# list of pairs: regex/lambda, the lambda takes url and beautiful soup object for page and returns a beautiful soup object
import smtplib
import subprocess
from BeautifulSoup import BeautifulSoup as bs

def filter_google(url, soup):
    return soup

def filter_with_readability(url, soup):
    """Run the page through an external program (in this case an
    interface to the node.js implementation of Arc 90's
    Readability."""
    p = subprocess.Popen(
        ['/home/albin/local/bin/node',
         '/home/albin/projects/readability/readability.js', 
         url],
    stdout, stderr = p.communicate(input=str(soup))
    return bs(stdout)
        
prefilter = [("http://(www.)?google.com(/)?.*", filter_google)]

# N.B. readability does some quite odd things, so we want to do this
#  as late in the mangling process as possible.
postfilter = [("http://.*", filter_with_readability)]

mail_from = "mail-web-page@localhost"
mail_to = "albin@localhost"

def send_mail(mfr, mto, msg):
    s = smtplib.SMTP('localhost')
    s.sendmail(mfr, mto, msg.as_string())
    s.quit()
