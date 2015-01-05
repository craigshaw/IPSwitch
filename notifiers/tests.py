#! /usr/bin/python

from nma import NotifyMyAndroidNotifier
import unittest
import datetime

class NMATests(unittest.TestCase):
    def setUp(self):
        self.notifier = NotifyMyAndroidNotifier('IPMon Test')

    def test_send_notification_sends(self):
        response = self.notifier.send_notification('Sent at {0}'.format(datetime.datetime.now()), 'Test Case')
        self.assertEqual(response, 'Expecting what here?')

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(NMATests)
    unittest.TextTestRunner(verbosity=2).run(suite)