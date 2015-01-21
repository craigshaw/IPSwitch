from urllib import urlencode
import urllib2
import json
import config

api_url = 'https://api.pushbullet.com/v2/pushes'

class PushBulletProvider(object):
	""" PushBullet provider class. Exposes methods to push messages to pushbullet clients. Currently only supports sending of Notes """
	def __init__(self, application, access_token):
		super(PushBulletProvider, self).__init__()
		self.application = application
		self.access_token = access_token

	def send_notification(self, message, event):
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
		password_mgr.add_password(None, api_url, self.access_token, '')
		authhandler = urllib2.HTTPBasicAuthHandler(password_mgr)
		opener = urllib2.build_opener(authhandler)
		urllib2.install_opener(opener)
		message_payload = self._build_message('{0}: {1}'.format(self.application, event), message)
		request = urllib2.Request(api_url, message_payload, {'Content-Type': 'application/json'})
		response = urllib2.urlopen(request)
		config.logger.debug('PushBullet Response: {0}'.format(response.read()))

	def _build_message(self, event, message):
		return json.dumps({'type': 'note', 'title': event, 'body': message})