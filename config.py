""" IPSwitch global config file """

from providers.WMIPCom import WMIPComProvider
from providers.RealIPInfo import RealIPInfoProvider
from notifiers.nma import NotifyMyAndroidNotifier
import logging

# Logger(s)
logger = None

# Providers
providers = {"whatsmyip.com": WMIPComProvider(),
"realip.info": RealIPInfoProvider()}

# Notifiers
notifier = NotifyMyAndroidNotifier('IP Monitor')

# General
pid_file = '/var/run/ipmonitor.pid'

def configure_logging():
    global logger
    logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger('apscheduler.scheduler').setLevel(logging.CRITICAL)
    logging.getLogger('apscheduler.threadpool').setLevel(logging.CRITICAL)
    logger = logging.getLogger('ipmonitor')
    logger.addHandler(logging.StreamHandler())