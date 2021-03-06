"""
See COPYING for license information.
"""
import os.path
import socket

from twisted.trial import unittest
from twisted.internet import threads, defer

from swftp.sftp.service import makeService, Options


TEST_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class SFTPServiceTest(unittest.TestCase):

    @defer.inlineCallbacks
    def setUp(self):
        opts = Options()
        opts.parseOptions([
            '--config_file=%s' % os.path.join(TEST_PATH, 'test-sftp.conf'),
            '--priv_key=%s' % os.path.join(TEST_PATH, 'test_id_rsa'),
            '--pub_key=%s' % os.path.join(TEST_PATH, 'test_id_rsa.pub'),
        ])
        self.service = makeService(opts)
        yield self.service.startService()

    def tearDown(self):
        return self.service.stopService()

    def _defer_test_service_listen(self):
        for n in range(1000):
            sock = socket.socket()
            sock.connect(('127.0.0.1', 6022))

    def test_service_listen(self):
        return threads.deferToThread(self._defer_test_service_listen)
