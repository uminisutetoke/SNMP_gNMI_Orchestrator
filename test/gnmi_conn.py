from pygnmi.client import gNMIclient

# Variables
host1 = {"ip_address": "172.80.80.21", "port": 57401,
        "username": "admin", "password": "NokiaSrl1!"}

# Body
if __name__ == '__main__':
    with gNMIclient(
        target=(host1["ip_address"], host1["port"]),
        username=host1["username"],
        password=host1["password"],
        # debug=True,
        insecure=True,
        skip_verify=True,
        ) as gc:
        result = gc.capabilities()
        #result = gc.get(path=['/system/grpc-server[name=insecure-mgmt]/'])

    print(result)
