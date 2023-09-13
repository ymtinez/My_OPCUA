# My_OPCUA

### OPCUA-python: 
Project to simulate an OPC-UA server and client using a Python library.

### OPCUA-SiemensPLC:
Project for connecting to a Siemens S7-1500 PLC via  OPC-UA Server to read and write values from databases. It includes the ability to list all databases on the server and their respective variables.
#
Using:
Pure Python OPC UA / IEC 62541 Client and Server Python 2, 3 and pypy.
http://freeopcua.github.io/, https://github.com/FreeOpcUa/python-opcua
#

# Installation

### Manual
With pip (note: the package was ealier called freeopcua)

Windows:

    pip install opcua

Ubuntu:

    apt install python-opcua        # Library
    apt install python-opcua-tools  # Command-line tools

### Automaticly
Using requirement.txt file:

    pip install -r requirements.txt