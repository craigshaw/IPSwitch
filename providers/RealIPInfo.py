import urllib2
import json

class RealIPInfoProvider(object):
	"""docstring for WMIPOrgProvider"""
	def __init__(self):
		super(RealIPInfoProvider, self).__init__()
		
	def get_external_ip(self):
		req = urllib2.Request('http://www.realip.info/api/p/realip.php')
		r = urllib2.urlopen(req)
		data = json.loads(r.read())
		return data["IP"]