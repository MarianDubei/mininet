from mininet.util import pexpect

import os
import pytest

prompt = 'mininet>'

def test_setup():
    '''
    Setup of mininet network. If hostonlynode run successfully, then
    prompt string value is expected to be met in the cli, i.e. cli_setup == 0
    '''
    pytest.net = pexpect.spawn('python -m hostonlynode')
    try:
        cli_setup = pytest.net.expect(prompt)
    except: cli_setup = -1
    assert cli_setup == 0

def test_pingall():
    '''
    Ping all hosts in the network using the standart mininet API. Expected result is
    parsed and percentage of failed ping requests is being accounted.
    '''
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
    '''
    Ping reciprocal hosts h1->h2 and h2->h1. Expected
    failure rate is 0 (percent value).
    '''
    pytest.net.expect(prompt)
    pytest.net.sendline('%s ping -c 1 %s' % (hostname1, hostname2))
    pytest.net.expect('(\d+)% packet loss')
    percent = int(pytest.net.match.group(1)) if pytest.net.match else -1
    assert percent == 0

@pytest.mark.parametrize("hostname,ip", [
    ('h1', '192.168.56.103'),
])
def test_host_ping_ip_absent(hostname, ip):
    '''
    Ping unreachable host with IP address 192.168.56.103 with default
    mininet API. As this IP is missing a failure rate is expected to be 100%
    '''
    pytest.net.expect(prompt)
    pytest.net.sendline('%s ping -c 1 %s' % (hostname, ip))
    pytest.net.expect('(\d+)% packet loss')
    percent = int(pytest.net.match.group(1)) if pytest.net.match else -1
    assert percent == 100

@pytest.mark.parametrize("host_ip", [
    ('10.0.0.1'),
    ('10.0.0.2'),
])
def test_os_ping_host(host_ip):
    '''
    Ping network hosts with IPs 10.0.0.1 and 10.0.0.2
    from the host OS. Required response is 0 (success)
    '''
    response = os.system("ping -c 1 " + host_ip)
    assert response == 0

def test_exit():
    '''
    Send quit command to mininet network and wait
    for the shut down
    '''
    pytest.net.sendline('quit')
    pytest.net.wait()
