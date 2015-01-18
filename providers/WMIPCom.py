import urllib2
from bs4 import BeautifulSoup

class WMIPComProvider(object):
    """ IP resolution provider for whatismyip.com """
    def __init__(self):
        super(WMIPComProvider, self).__init__()
        
    def get_external_ip(self):
        currentIP = ''
        req = urllib2.Request('http://www.whatismyip.com/')
        req.add_header('User-Agent', 'Mozilla/5.0')
        r = urllib2.urlopen(req)
        parser = BeautifulSoup(r.read())
        tag = parser.find(self._ip_finder)               
        for child in tag.children:
            currentIP += child.string
        return currentIP

    def _ip_finder(self, tag):
        return tag.name == 'div' and tag.has_attr('class') and tag['class'][0] == u'the-ip'