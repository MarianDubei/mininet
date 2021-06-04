from mininet.util import pexpect

import pytest

prompt = 'mininet>'

def test_setup():
    pytest.net = pexpect.spawn('python -m hostonlynode')
    try:
        cli_setup = pytest.net.expect(prompt)
    except: cli_setup = -1
    assert cli_setup == 0

def test_pingall():
    pytest.net.sendline( 'pingall' )
    pytest.net.expect ( '(\d+)% dropped' )
    print('(\d+)% dropped')
    percent = int( pytest.net.match.group( 1 ) ) if pytest.net.match else -1
    assert percent == 0

@pytest.mark.parametrize("hostname1,hostname2", [
    ('h1', 'h2'),
    ('h2', 'h1'),
])
def test_host_ping_ip_reachable(hostname1, hostname2):
    pytest.net.expect(prompt)
    pytest.net.sendline('%s ping -c 1 %s' % (hostname1, hostname2))
    pytest.net.expect('(\d+)% packet loss')
    percent = int(pytest.net.match.group(1)) if pytest.net.match else -1
    assert percent == 0

@pytest.mark.parametrize("hostname,ip", [
    ('h1', '192.168.56.103'),
])
def test_host_ping_ip_absent(hostname, ip):
    pytest.net.expect(prompt)
    pytest.net.sendline('%s ping -c 1 %s' % (hostname, ip))
    pytest.net.expect('(\d+)% packet loss')
    percent = int(pytest.net.match.group(1)) if pytest.net.match else -1
    assert percent == 100

def test_exit():
    pytest.net.sendline('quit')
    pytest.net.wait()
