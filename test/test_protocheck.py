import sys
sys.path.append('..')

import pytest
from main.protocolcheck import ProtocolCheck

test_targets = [
    {
        "ip_address": "172.80.80.21",
        "username": "admin",
        "password": "NokiaSrl1!"
    }
]


def test_run():
    pass

def test_gnmi_available():
    p = ProtocolCheck(test_targets)
    p.targets = test_targets[0]
    assert True == p.gnmi_available(57401)

def test_snmp_available():
    pass

def test_insecure_device():
    pass
