"""Using my_opcua_client to read all variables"""
import time
from my_opcua_client import OPCUAClient

URL = "opc.tcp://192.168.0.82:4840"
client = OPCUAClient(URL)

if client.connect():
    while True:
        client.get_variables()
        time.sleep(1)
