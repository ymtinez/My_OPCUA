"""Reading and writing opcua dbs"""
import asyncio
from asyncua import Client, ua


async def read_input_value(client_connection: Client, node_id: str) -> None:
    """Function to read value from OPCUA-Server

    Args:
        client_connection (Client): OPCUA client object
        node_id (string): Node identification: "ns=<namespaceIndex>;s=<stringIdentifier>"
    """
    client_node = client_connection.get_node(node_id)  # get node
    client_node_value = await client_node.get_value()  # read node value
    client_node_name = str(await client_node.read_display_name())[33:-2]
    if isinstance(client_node_value, list):
        for index, value in enumerate(client_node_value):
            print(
                f"Values of: {client_node_name}[{index}] ({client_node}): {round(value,2) if isinstance(value, float) else value}"
            )
    else:
        print(
            f"Value of: {client_node_name} ({client_node}) : {round(client_node_value,2) if isinstance(client_node_value, float) else client_node_value}"
        )


async def get_variable_type(client_connection: Client, node_id: str) -> str:
    """Function to get the type of the specific variable from node_id

    Args:
        client_connection (Client): OPCUA client object
        node_id (string): Node identification: "ns=<namespaceIndex>;s=<stringIdentifier>"

    Returns:
        str: "Real" if Type.float, "Int" if Type.int, "Boolean" if Type.bool, "" if not exist
    """
    client_node = client_connection.get_node(node_id)  # get node
    client_node_value = await client_node.get_value()
    if isinstance(client_node_value, float):
        return "Real"
    elif isinstance(client_node_value, bool):
        return "Boolean"
    elif isinstance(client_node_value, int):
        return "Int"
    else:
        return ""


async def write_value_int(client_connection: Client, node_id: str, value: int) -> None:
    """Function to write integer value in the specific node_id from OPCUA-Server

    Args:
        client_connection (Client): OPCUA client object
        node_id (string): Node identification: "ns=<namespaceIndex>;s=<stringIdentifier>"
        value (int): Value to be write in the specific node_id
    """
    client_node = client_connection.get_node(node_id)  # get node
    client_node_value_ua = ua.DataValue(ua.Variant(value, ua.VariantType.Int16))
    await client_node.set_value(client_node_value_ua)
    client_node_name = str(await client_node.read_display_name())[33:-2]
    print(f"New value of: {client_node_name} ({client_node}): {value}")


async def write_value_real(client_connection: Client, node_id: str, value: float) -> None:
    """Function to write real value in the specific node_id from OPCUA-Server

    Args:
        client_connection (Client): OPCUA client object
        node_id (string): Node identification: "ns=<namespaceIndex>;s=<stringIdentifier>"
        value (real): Value to be write in the specific node_id
    """
    client_node = client_connection.get_node(node_id)  # get node
    client_node_value_ua = ua.DataValue(ua.Variant(value, ua.VariantType.Float))
    await client_node.set_value(client_node_value_ua)
    client_node_name = str(await client_node.read_display_name())[33:-2]
    print(f"New value of: {client_node_name} ({client_node}): {value}")


async def write_value_bool(client_connection: Client, node_id: str, value: bool) -> None:
    """Function to write boolean value in the specific node_id from OPCUA-Server

    Args:
        client_connection (Client): OPCUA client object
        node_id (string): Node identification: "ns=<namespaceIndex>;s=<stringIdentifier>"
        value (real): Value to be write in the specific node_id
    """
    client_node = client_connection.get_node(node_id)  # get node
    client_node_value_ua = ua.DataValue(ua.Variant(value, ua.VariantType.Boolean))
    await client_node.set_value(client_node_value_ua)
    client_node_name = str(await client_node.read_display_name())[33:-2]
    print(f"New value of: {client_node_name} ({client_node}): {client_node_value_ua}")


async def get_specific_db_node_id(client_connection: Client, db_name: str) -> str:
    """Getting the node id of the specific DataBase

    Args:
        client_connection (Client): OPCUA client object
        db_name (str): name of the specific DataBase

    Returns:
        str: Node identification: "ns=<namespaceIndex>;s=<stringIdentifier>"
    """
    data_block_global = client_connection.get_node("ns=3;s=DataBlocksGlobal")
    databases = await data_block_global.get_children()
    for database in databases:
        if str(await database.read_display_name())[33:-2].lower() == db_name.lower():
            return str(database)
    return ""


async def read_all_of_db(client_connection: Client, db_node_id: str) -> None:
    """Print all variables into de specific database

    Args:
        client_connection (Client): OPCUA client object
        db_name (str): name of the specific DataBase
    """
    database_node = client_connection.get_node(db_node_id)
    database_name = str(await database_node.read_display_name())[33:-2]
    if db_node_id == "":
        print(f"The specific DB: {database_name} not exist")
    else:
        print(f"Node_ID of {database_name} is: {db_node_id}")
        db_node = client_connection.get_node(db_node_id)
        variables = await db_node.get_variables()
        print(f"******************** {database_name} ********************")
        for variable in variables:
            await read_input_value(client_connection, variable)
        print("*" * len(f"******************** {database_name} ********************"))


async def read_all_dbs(client_connection: Client) -> None:
    """Print all variables of all databases

    Args:
        client_connection (Client): OPCUA client object
    """
    data_block_global = client_connection.get_node("ns=3;s=DataBlocksGlobal")
    databases = await data_block_global.get_children()
    print("*************** All Databases ***************")
    for database in databases:
        if str(await database.read_display_name())[33:-2] != "Icon":  # Skip Icon element
            await read_all_of_db(client_connection, database)
    print("*" * 44)


async def list_all_databases(client_connection: Client) -> None:
    """Show the list of all databases in the server

    Args:
        client_connection (Client): OPCUA client object
    """
    data_block_global = client_connection.get_node("ns=3;s=DataBlocksGlobal")
    databases = await data_block_global.get_children()
    print("************* List of Databases *************")
    for database in databases:
        if (
            database_name := str(await database.read_display_name())[33:-2]
        ) != "Icon":  # Skip Icon element
            print(f" -> {database_name}")
    print("*" * 44)


def str2bool(value: str) -> bool:
    """Function to convert from string to bool

    Args:
        value (str): value to convert ("1", "True", "true", "T", "t")

    Returns:
        bool: True if value in ("1", "True", "true", "T", "t")
    """
    return value.lower() in ("1", "true", "t")


async def main():
    """Main function for this app"""
    print("This app allow to read values from OPCUA-Server of SIEMENS S7-1500")
    url = input("Enter the url of the server (opc.tcp://<IP_OPCUA-SERVERr>:<PORT>): ")
    # url = "opc.tcp://192.168.0.120:4840"
    # client = Client("opc.tcp://192.168.0.120:4840")
    async with Client(url) as client:
        try:
            option = ""
            while option.lower() not in ["q"]:
                print("=" * 60)
                print(f"Client connected with {url}")
                print("Select an option from the list")
                print("1. Lists Databases in the server")
                print("2. Show values from specific database")
                print("3. Show values from all databases")
                print("4. Write value")
                print("Press 'q' and 'ENTER' to exit")
                option = input("Enter the option: ")
                if option in ["1", "2", "3", "4"]:
                    if option == "1":
                        await list_all_databases(client)
                    elif option == "2":
                        specific_db_name = input("Enter the name of the specific DB: ")
                        specific_db_node_id = await get_specific_db_node_id(
                            client, specific_db_name
                        )
                        await read_all_of_db(client, specific_db_node_id)
                    elif option == "3":
                        await read_all_dbs(client)
                    else:
                        print("*" * 45)
                        variable_node_id = input(
                            "Enter the node_id of the variable (ns=<namespaceIndex>;s=<stringIdentifier>): "
                        )
                        variable_type = await get_variable_type(client, variable_node_id)
                        if variable_type == "":
                            print("Impossible to find that variable")
                        else:
                            await read_input_value(client, variable_node_id)
                            if variable_type == "Real":
                                variable_value = float(
                                    input(
                                        f"The variable is type: {variable_type} (#.#), Enter the value: "
                                    )
                                )
                                await write_value_real(
                                    client, variable_node_id, variable_value
                                )
                            elif variable_type == "Int":
                                variable_value = int(
                                    input(
                                        f"The variable is type: {variable_type} (#), Enter the value: "
                                    )
                                )
                                await write_value_int(
                                    client, variable_node_id, variable_value
                                )
                            elif variable_type == "Boolean":
                                print(
                                    f'The variable is type: {variable_type} (for "True" enter: ("1", "True", "true", "T", "t"), else "False")'
                                )
                                variable_value = str2bool(input("Enter the value: "))
                                await write_value_bool(
                                    client, variable_node_id, variable_value
                                )
                elif option.lower() not in ["q"]:
                    print("You entered wrong option")
                    option = input(
                        "Press 'q' and 'ENTER' to exit or 'ENTER' to read again: "
                    )
        finally:
            print("Thank you")


if __name__ == "__main__":
    asyncio.run(main())
