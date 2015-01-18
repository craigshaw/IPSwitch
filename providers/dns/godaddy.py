"""
 DNS Provider wrapping Godaddy's web interface. Currently supports the following,
 - Updating of A record
"""

import mechanize, cookielib
import config

go_daddy_landing_page = 'https://dns.godaddy.com'
zone_editor_url = 'https://dns.godaddy.com/ZoneFile.aspx?zone={0}&zoneType=0&sa='

# https://dns.godaddy.com/ZoneFile_WS.asmx/EditRecordField
# POSTs this payload:
edit_record_endpoint = 'https://dns.godaddy.com/ZoneFile_WS.asmx/EditRecordField'
edit_record_payload = '{\"sInput\":\"<PARAMS><PARAM name=\\\"type\\\" value=\\\"arecord\\\" /><PARAM name=\\\"fieldName\\\" value=\\\"data\\\" /><PARAM name=\\\"fieldValue\\\" value=\\\"**IP**\\\" /><PARAM name=\\\"lstIndex\\\" value=\\\"0\\\" /></PARAMS>\"}'

# https://dns.godaddy.com/ZoneFile_WS.asmx/SaveRecords
# POSTs this payload:
save_record_endpoint = 'https://dns.godaddy.com/ZoneFile_WS.asmx/SaveRecords'
save_record_payload = '{\"sInput\":\"<PARAMS><PARAM name=\\\"domainName\\\" value=\\\"**DOMAIN**\\\" /><PARAM name=\\\"zoneType\\\" value=\\\"0\\\" />\
<PARAM name=\\\"aRecEditCount\\\" value=\\\"1\\\" /><PARAM name=\\\"aRecDeleteCount\\\" value=\\\"0\\\" /><PARAM name=\\\"aRecEdit0Index\\\" value=\\\"0\\\" />\
<PARAM name=\\\"cnameRecEditCount\\\" value=\\\"0\\\" /><PARAM name=\\\"cnameRecDeleteCount\\\" value=\\\"0\\\" /><PARAM name=\\\"mxRecEditCount\\\" value=\\\"0\\\" />\
<PARAM name=\\\"mxRecDeleteCount\\\" value=\\\"0\\\" /><PARAM name=\\\"txtRecEditCount\\\" value=\\\"0\\\" /><PARAM name=\\\"txtRecDeleteCount\\\" value=\\\"0\\\" />\
<PARAM name=\\\"srvRecEditCount\\\" value=\\\"0\\\" /><PARAM name=\\\"srvRecDeleteCount\\\" value=\\\"0\\\" /><PARAM name=\\\"aaaaRecEditCount\\\" value=\\\"0\\\" />\
<PARAM name=\\\"aaaaRecDeleteCount\\\" value=\\\"0\\\" /><PARAM name=\\\"soaRecEditCount\\\" value=\\\"0\\\" /><PARAM name=\\\"soaRecDeleteCount\\\" value=\\\"0\\\" />\
<PARAM name=\\\"nsRecEditCount\\\" value=\\\"0\\\" /><PARAM name=\\\"nsRecDeleteCount\\\" value=\\\"0\\\" /></PARAMS>\"}'

class GodaddyDNSProvider(object):
	"""Exposes programmtic interface over Godaddy's web interface for managing DNS. Currently exposes a limited set of functions including
- Updating of A record
	"""
	def __init__(self, credentials):
		super(GodaddyDNSProvider, self).__init__()
		self.credentials = credentials

	def update_a_record(self, domain, a_record_ip):
		try:
			browser = self._create_browser()

			# Go to the landing page
			self._navigate_to_landing_page(browser)
			
			# Login
			self._login(browser, self.credentials['username'], self.credentials['password'])

			# With our logged in session, navigate to the zone editor for our domain
			self._navigate_to_zone_editor(browser, domain)

			# Now manipulate controls to update A record
			self._edit_a_record(browser, a_record_ip)

			self._save_a_record(browser, domain)

			# All done :)
			config.logger.debug('Successfully updated A record to {0}'.format(a_record_ip))
		except Exception as e:
			config.logger.error('Error: {0}'.format(e))

	def _navigate_to_landing_page(self, browser):
		self._navigate_to_url(browser, go_daddy_landing_page)

	def _navigate_to_zone_editor(self, browser, domain):
		self._navigate_to_url(browser, zone_editor_url.format(domain))

	def _navigate_to_url(self, browser, url):
		config.logger.debug('Navigating to {0}'.format(url))
		page = browser.open(url)
		config.logger.debug('Response code: {0}'.format(page.code))
		return page

	def _login(self, browser, username, password):
		config.logger.debug('Completing login form...')
		browser.select_form(nr=1)  # Select form at index 1 (2nd form)
		browser.form['loginname'] = username
		browser.form['password'] = password
		config.logger.debug('Submitting login...')
		page = browser.submit()
		config.logger.debug('Login response code: {0}'.format(page.code))

	def _edit_a_record(self, browser, new_ip):
		# POST to edit record endpoint
		data = edit_record_payload.replace('**IP**', new_ip)
		self._post_json_data_to_url(browser, edit_record_endpoint, data)

	def _save_a_record(self, browser, domain):
		# Now POST to the SaveRecord endpoint
		data = save_record_payload.replace('**DOMAIN**', domain)
		self._post_json_data_to_url(browser, save_record_endpoint, data)

	def _post_json_data_to_url(self, browser, url, data):
		config.logger.debug('POST data: {0}'.format(data))
		request = mechanize.Request(url, data=data, headers={'Content-Type': 'application/json; charset=UTF-8'})
		page = browser.open(request)
		config.logger.debug('Response code: {0}'.format(page.code))
		config.logger.debug('Response: {0}'.format(page.read()))

	def _create_browser(self):
		br = mechanize.Browser()
		br.set_handle_robots(False)   # Ignore robots
		br.set_handle_refresh(False)
		# User-Agent - Chrome 41.0.2228.0
		br.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
		br.cookie_jar = cookielib.LWPCookieJar()
		br.set_cookiejar(br.cookie_jar)
		return br
	