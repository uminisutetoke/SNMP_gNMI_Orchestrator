import pytest
from main import protocolcheck


p = protocolcheck([
    {"ip_address": "172.80.80.21",
    "username": "admin", "password": "NokiaSrl1!"}
])
def test_gnmi_available(p):
    p.run()
    print(p.inventory)
