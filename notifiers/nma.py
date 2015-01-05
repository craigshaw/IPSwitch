"""
Notify My Android provider class. Simple utility for sending push messages to a given
NMA application key
"""
from urllib import urlencode
import urllib2
import logging

notificationKey = "<your_key>"
notificationRoot = "https://www.notifymyandroid.com/publicapi/notify"

class NotifyMyAndroidNotifier(object):
	def __init__(self, application):
		super(NotifyMyAndroidNotifier, self).__init__()
		self.application = application

	def send_notification(self, message, event):
		data = urlencode([('apikey',notificationKey),('application',self.application),('event',event),('description',message)])    
		request = urllib2.Request(url=notificationRoot, data=data)
		f = urllib2.urlopen(request)
		return f.read()
		#logger.debug('NMA Response: {0}'.format(response))