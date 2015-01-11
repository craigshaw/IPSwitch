""" IPSwitch global config file """

from providers.WMIPCom import WMIPComProvider
from providers.RealIPInfo import RealIPInfoProvider
from notifiers.nma import NotifyMyAndroidNotifier
import logging

# General
pid_file = '/var/run/ipmonitor.pid'
application_name = 'IPSwitch'

# Logger(s)
logger = None

# Providers
providers = {"whatsmyip.com": WMIPComProvider(),
"realip.info": RealIPInfoProvider()}

# Notifiers
nma_key = "<your_key>"
notifier = NotifyMyAndroidNotifier(application_name, nma_key)

def configure_logging():
    global logger
    logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger('apscheduler.scheduler').setLevel(logging.CRITICAL)
    logging.getLogger('apscheduler.threadpool').setLevel(logging.CRITICAL)
    logger = logging.getLogger('ipmonitor')

def add_logging_stream_handler():
	logger.addHandler(logging.StreamHandler())