'''OPC UA Server Simulate'''
from random import randint
import datetime
import time
from opcua import Server

server = Server()

URL = "opc.tcp://192.168.0.82:4840"
server.set_endpoint(URL)

NAME = "OPCUA_SIMULATE_SERVER"
addspace = server.register_namespace(NAME)
print(f"namespace: {addspace}")

node = server.get_objects_node()
print(f"node: {node}")

param = node.add_object(addspace, "Parameters")
print(f"param: {param}")

Temp = param.add_variable(addspace, "Temperature", 0)
print(f"Temp: {Temp}")
Press = param.add_variable(addspace, "Pressure", 0)
print(f"Press: {Press}")
Time = param.add_variable(addspace, "Time", 0)
print(f"Time: {Time}")

boiler = node.add_object(addspace, "Boiler")
print(f"boiler: {boiler}")

TempBoiler = boiler.add_variable(addspace, "TemperatureBoiler", 0)
print(f"TempBoiler: {TempBoiler}")

Visc = param.add_variable(addspace, "Viscosity", 0)
print(f"Visc: {Visc}")

Temp.set_writable()
Press.set_writable()
Time.set_writable()
TempBoiler.set_writable()
Visc.set_writable()

# addspaceTest = server.register_namespace("Test")
# print(f"namespaceTest: {addspaceTest}")

# boiler = node.add_object(addspaceTest, "Boiler")
# print(f"boiler: {boiler}")

# TempBoiler = boiler.add_variable(addspaceTest, "TemperatureBoiler", 0)
# print(f"TempBoiler: {TempBoiler}")

server.start()
print(f"Server started at {URL}")

while True:
    # Creating sumulation values
    Temperature = randint(10, 50)
    Pressure = randint(200, 999)
    TIME = datetime.datetime.now()
    TemperatureBoiler = randint(200, 450)
    Viscosity = randint(10, 20)
    # Showing values
    print(
        f"Server: Temp={Temperature}, Pressure={Pressure}, Time={TIME}, TempBoiler={TemperatureBoiler}, Visc={Viscosity}")
    # Sending values tu the server
    Temp.set_value(Temperature)
    Press.set_value(Pressure)
    Time.set_value(TIME)
    TempBoiler.set_value(TemperatureBoiler)
    Visc.set_value(Viscosity)
    # Sleep 2s
    time.sleep(2)
