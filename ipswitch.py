#! /usr/bin/env python

""" IPSwitch - Monitors external IP, detects changes and automates subsequent actions """

from apscheduler.scheduler import Scheduler
from daemon.daemon import Daemon
import sys
import time
import config

scheduler = Scheduler()

class IPSwitch(Daemon):
    def run(self):
        try:
            self.bootstrap()

            # Not sure I like this, but not sure what a more elegant solution is...
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit) as e:
            pass

    def bootstrap(self):
        # Get and store current IP
        self.provider = config.providers["realip.info"]
        self.current_ip = self.provider.get_external_ip()

        config.logger.info('Current IP: {0}'.format(self.current_ip))

        # Start update timer
        scheduler.add_interval_job(self.review_current_ip, seconds=300)
        scheduler.start()

    def get_external_ip(self):
        try:
            external_ip = self.provider.get_external_ip()
        except Exception as e:
            config.logger.error('Failed to retrieve external IP: {0}'.format(e))
            external_ip = 'Unknown'

        return external_ip

    def review_current_ip(self):
        new_ip = self.get_external_ip()
        config.logger.debug('Got current IP address: {0}'.format(new_ip))

        if new_ip != 'Unknown' and new_ip != self.current_ip:
            config.logger.info('IP address changed from {0} to {1}'.format(self.current_ip, new_ip))
            config.notifier.send_notification('IP address changed from {0} to {1}'.format(self.current_ip, new_ip), 'IP Update')
            self.current_ip = new_ip

if __name__ == '__main__':
    ipmonitor = IPSwitch(config.pid_file)
    spawning_daemon = True
    config.configure_logging()

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            ipmonitor.start()
        elif 'stop' == sys.argv[1]:
            ipmonitor.stop()
        elif 'restart' == sys.argv[1]:
            ipmonitor.restart()
        elif 'test' == sys.argv[1]:
            spawning_daemon = False
            ipmonitor.run()
        else:
            print "Unknown command"
            sys.exit(2)

        if spawning_daemon:
            sys.exit(0)
    else:
        print "usage: {0} start|stop|restart|test".format(sys.argv[0])
        sys.exit(2)
