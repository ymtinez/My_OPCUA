'''
My OPCUA Client Class to connect with OPCUA-Server and read all variables
'''
from opcua import Client


class OPCUAClient:
    """My OPCUA Client to connect with an OPCUA-Server

    This class allow to connect with an OPC UA-Server and read all nodes and respective variables
    """

    def __init__(self, url) -> None:
        """Defining URL for connection

        Args:
            url (string): opc.tcp://<IP_OPCUA_SERVER>:<PORT>
        """
        self.is_connected = False
        self.url = url
        self.client = Client(self.url)
        self.namespaces = []
        self.objects = []
        self.nodes = []

    def connect(self) -> bool:
        """Connect with the server
        """
        try:
            self.client.connect()
            print("Client connected")
            self.namespaces = self.client.get_namespace_array()
            self.objects = self.client.get_objects_node()
            self.nodes = self.objects.get_children()
            return True
        except Exception as err:
            print(f"Error in the connection: {err}")
            return False

    def get_variables(self) -> None:
        """This function connect with the server and read all variables
        """
        print("***** Reading variables *****")
        for index_node in range(1, len(self.nodes)):
            # First node don't needed
            # Getting each node from nodes_list
            node = self.objects.get_children()[index_node]
            # Getting the name of the node
            node_name = str(node.get_browse_name())[16:-1]
            # Printing node_name: {node_value}
            print(f"{node_name}: {node}")
            # Getting the list of variables into the node
            variables = node.get_children()
            for index_variable in range(len(variables)):
                # Getting each variable from variables list
                variable = node.get_children()[index_variable]
                # Getting the name of the variable
                variable_name = str(variable.get_browse_name())[16:-1]
                # Getting variable value
                variable_value = variable.get_value()
                # Printing variable_name: {variable_value}
                print(f" -> {variable_name}: {variable_value}")
        print("*"*29)
