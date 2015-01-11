"""
Notify My Android provider class. Simple utility for sending push messages to a given
NMA application key
"""
from urllib import urlencode
import urllib2
import logging
import config

notificationRoot = "https://www.notifymyandroid.com/publicapi/notify"

class NotifyMyAndroidNotifier(object):
	def __init__(self, application, nma_key):
		super(NotifyMyAndroidNotifier, self).__init__()
		self.application = application
		self.nma_key = nma_key

	def send_notification(self, message, event):
		data = urlencode([('apikey',self.nma_key),('application',self.application),('event',event),('description',message)])    
		request = urllib2.Request(url=notificationRoot, data=data)
		f = urllib2.urlopen(request)
		response = f.read()
		config.logger.debug('NMA Response: {0}'.format(response))