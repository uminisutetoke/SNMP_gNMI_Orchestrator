from pygnmi.client import gNMIclient

# Variables
host = ('172.20.20.4', '57400')

# Body
if __name__ == '__main__':
    with gNMIclient(
        target=host,
        username='admin',
        password='NokiaSrl1!',
        insecure=True
        ) as gc:
            result = gc.get(path=['openconfig-interfaces:interfaces', 'openconfig-acl:acl'])

    print(result)
