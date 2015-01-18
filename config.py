""" IPSwitch global config file """

from providers.WMIPCom import WMIPComProvider
from providers.RealIPInfo import RealIPInfoProvider
from notifiers.nma import NotifyMyAndroidNotifier
from providers.dns.godaddy import GodaddyDNSProvider
import logging

# General
pid_file = '/var/run/ipswitch.pid'
application_name = 'IPSwitch'
refresh_interval = 300 # seconds

# Logger(s)
logger = None

# Providers
providers = {'whatsmyip.com' : WMIPComProvider(),
'realip.info': RealIPInfoProvider()}

# DNS Providers
go_daddy_creds = {'username' : '<your_username>', 'password' : '<your_password>'} # This needs externalising
dns_providers = {'godaddy' : GodaddyDNSProvider(go_daddy_creds)}

# Notifiers
nma_key = '<your_key>' # This needs externalising
notifier = NotifyMyAndroidNotifier(application_name, nma_key)

def configure_logging():
    global logger
    logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger('apscheduler.scheduler').setLevel(logging.CRITICAL)
    logging.getLogger('apscheduler.threadpool').setLevel(logging.CRITICAL)
    logger = logging.getLogger('ipswitch')

def add_logging_stream_handler():
	logger.addHandler(logging.StreamHandler())