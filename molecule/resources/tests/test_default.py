import os
import sys

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_file_mode(host):
    keystore = host.file('/root/instance.p12')
    assert keystore.exists
    if sys.version_info[0] <= (2):
        assert oct(keystore.mode) == '0600'
    else:
        assert oct(keystore.mode) == '0o600'
    assert keystore.is_file


def test_version(host):
    cmd = host.command('openssl pkcs12 -info -in /root/instance.p12 -passin pass: -nokeys')
    assert cmd.rc == 0
    assert 'friendlyName: instance' in cmd.stdout
