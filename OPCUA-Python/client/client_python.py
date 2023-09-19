"""Using my_opcua_client to read all variables"""
import asyncio
from asyncua import Client


async def main():
    url = "opc.tcp://192.168.0.82:4840"
    async with Client(url) as client:
        print("Connected")
        namespaces = await client.get_namespace_array()
        objects = await client.nodes.objects.get_children()
        # nodes = await

        print("***** Reading variables *****")
        print("*** Namespaces: ***")
        for index in range(2, len(namespaces)):
            print(f" - {namespaces[index]}")
        while True:
            print("*" * 30)
            print("*** Objects: ***")
            for index in range(2, len(objects)):
                node = client.get_node(objects[index])
                node_name = str(await node.read_display_name())[33:-2]
                print(f"Node: {node}, Node_name: {node_name}")
                variables = await node.get_variables()
                for var in variables:
                    variable = client.get_node(var)
                    variable_name = str(await variable.read_display_name())[33:-2]
                    variable_value = await variable.get_value()
                    print(
                        f"    -> {variable_name} : {variable_value if not isinstance(variable_value, float) else round(variable_value, 2)}"
                    )
            print("*" * 30)
            await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())
