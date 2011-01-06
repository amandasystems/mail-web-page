# list of pairs: regex/lambda, the lambda takes url and beautiful soup object for page and returns a beautiful soup object
import smtplib

def filter_google(url, soup):
    return soup
    

prefilter = [("http://(www.)?google.com(/)?.*", filter_google),
             ("http://.*", lambda url, soup: soup)]

postfilter = []

mail_from = "mail-web-page@localhost"
mail_to = "albin@localhost"

def send_mail(mfr, mto, msg):
    s = smtplib.SMTP('localhost')
    s.sendmail(mfr, mto, msg.as_string())
    s.quit()
