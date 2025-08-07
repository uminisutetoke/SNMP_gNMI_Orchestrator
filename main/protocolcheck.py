import subprocess
from pygnmi.client import gNMIclient
from pysnmp.hlapi import *

class ProtocolCheck:
    def __init__(self, targets):
        self.targets = targets
        self.inventory = {} # チェック結果をここに保存

    def run(self):
        for t in self.targets:
            if not self.snmp_available(t):
                self.inventory["unknown"] = t
                break
            if self.insecure_device(t):
                b = self.gnmi_available(t, 57401)
            else:
                b = self.gnmi_available(t, 57400)
            if b:
                self.inventory["available"] = t
            else:
                self.inventory["unavailable"] = t

    def gnmi_available(self, target, port):
        with gNMIclient(
            target=(target["ip_address"], port),
            username=target["username"],
            password=target["password"],
            #skip_verify=int(str(port)[::-1][0]),
            insecure=True,
            skip_verify=True
            ) as gc:
            print(gc.capabilities())
            return True#gc.capabilities()
    def snmp_available(self, target):
        return True
    def insecure_device(self, target):
        return True
