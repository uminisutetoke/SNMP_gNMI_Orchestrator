import sys
sys.path.append('..')

import pytest
from main.protocolcheck import ProtocolCheck

test_targets = [
    {
        "ip_address": "172.20.20.2",
        "username": "admin",
        "password": "NokiaSrl1!"
    }
]


def test_gnmi_available():
    p = ProtocolCheck(test_targets)
    p.run()
    print("finished")
    print(p.inventory)
