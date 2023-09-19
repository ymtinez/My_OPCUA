"""OPC UA Server Simulate"""
import random
import datetime
import asyncio
from asyncua import Server, ua


async def main():
    server = Server()
    await server.init()

    url = "opc.tcp://192.168.0.82:4840"
    server.set_endpoint(url)
    server.set_server_name("OPCUA Server Simulate")

    uri = "OPCUA_SIMULATE_SERVER"
    idx = await server.register_namespace(uri)
    print(f"namespace: {idx}")

    param = await server.nodes.objects.add_object(idx, "Parameters")
    print(f" param: {param}")

    temp = await param.add_variable(idx, "Temperature", ua.Int32(0))
    print(f"  - Temp: {temp}")
    await temp.set_writable()

    press = await param.add_variable(idx, "Pressure", ua.Float(0.0))
    print(f"  - Press: {press}")
    await press.set_writable()

    timestamp = await param.add_variable(idx, "Time", datetime.datetime.utcnow())
    print(f"  - Time: {timestamp}")
    await timestamp.set_writable()

    boiler = await server.nodes.objects.add_object(idx, "Boiler")
    print(f" boiler: {boiler}")

    boiler_temp = await boiler.add_variable(idx, "BoilerTemperature", ua.Int32(0))
    print(f"  - boiler_temp: {boiler_temp}")
    await boiler_temp.set_writable()

    boiler_status = await boiler.add_variable(idx, "BoilerStatus", ua.Boolean())
    print(f"  - boiler_status: {boiler_status}")
    await boiler_status.set_writable()

    visc = await param.add_variable(idx, "Viscosity", ua.Float(0.0))
    print(f"  - Visc: {visc}")
    await visc.set_writable()

    async with server:
        print(f"Server started at {url}")

        while True:
            # Creating sumulation values
            temperature_value = ua.Int32(random.randint(200, 400))
            pressure_value = ua.Float(round(random.randint(5, 15) + random.random(), 2))
            timestamp_value = datetime.datetime.now()
            boiler_temperature_value = ua.Int32(random.randint(200, 450))
            boiler_status_value = random.choice([True, False])
            viscosity_value = ua.Float(round(random.randint(10, 30) + random.random(), 2))
            # Showing values
            print(
                f"Server: Temp={temperature_value}, Pressure={pressure_value}, Time={timestamp_value}, Boiler_Temp={boiler_temperature_value}, BoilerStatus={boiler_status_value}, Visc={viscosity_value}"
            )
            # Sending values tu the server
            await temp.set_value(temperature_value)
            await press.set_value(pressure_value)
            await timestamp.set_value(timestamp_value)
            await boiler_temp.set_value(boiler_temperature_value)
            await boiler_status.set_value(boiler_status_value)
            await visc.set_value(viscosity_value)
            # Sleep 2s
            await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())
