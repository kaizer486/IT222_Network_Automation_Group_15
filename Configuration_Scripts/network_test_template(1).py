from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
# Start the required devices in GNS3 before running this script.
# Use only devices that are suitable sources for the required tests.
# Replace the host address and TELNET console ports with current GNS3 values.
devices = [
    {
        "name": "R1",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.92.128",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5016,  # Replace with the current R1 TELNET console port.
    },
    {
        "name": "Teller-PC1",
        "device_type": "generic_telnet",
        "host": "192.168.92.128",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5024,  # Replace with the current PC1 TELNET console port.
    },
    {
        "name": "LoanOfficer-PC1",
        "device_type": "generic_telnet",
        "host": "192.168.92.128",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5026,  # Replace with the current PC2 TELNET console port.
    },
]
# Use a list of lists so that tests can be assigned to specific devices.
# The first item in each inner list is the source device. The remaining
# items are scenario-specific tests to run from that device.
#
# A Layer-2 switch can originate IP tests only when it has a management
# SVI/IP configuration and a reachable gateway. Remove its test group when
# the assigned scenario does not configure switch management addressing.
testing_commands = [
    [
        "R1",
        "ping 10.16.16.2",
    ],
    [
        "Teller-PC1",
        "ping 192.168.161.10",
    ],
    [
        "LoanOfficer-PC1",
        "ping 192.168.171.10",
    ],
]
# Connect to each selected source device and run only its assigned tests.
for device in devices:
    connection = None
    device_name = device["name"]
    # Remove the name field because Netmiko does not use it.
    connection_details = {
        key: value
        for key, value in device.items()
        if key != "name"
    }
    # Find the testing-command list for the current source device.
    commands_for_device = []
    for command_group in testing_commands:
        if command_group[0] == device_name:
            commands_for_device = command_group[1:]
            break
    if not commands_for_device:
        print(f"\n{device_name}: No network tests have been assigned.")
        continue
    try:
        print(f"\nConnecting to {device_name}...")
        connection = ConnectHandler(**connection_details)
        # Enter privileged EXEC mode if an enable password is provided.
        if connection_details["secret"]:
            connection.enable()
        # Disable output paging on Cisco IOS devices only; VPCS PCs do not
        # support this command.
        if connection_details["device_type"] == "cisco_ios_telnet":
            connection.send_command("terminal length 0")
        for command in commands_for_device:
            print(f"\n--- {device_name}: Testing {command} ---")
            output = connection.send_command(
                command,
                read_timeout=30,
            )
            print(output)
    except NetmikoTimeoutException:
        print(
            f"{device_name}: Connection timed out. Check the GNS3 VM IP address, "
            "TELNET console port, GNS3 VM, and device state."
        )
    except NetmikoAuthenticationException:
        print(
            f"{device_name}: Authentication failed. Check the username, "
            "password, and enable password."
        )
    except Exception as error:
        print(f"{device_name}: Unexpected error: {error}")
    finally:
        if connection is not None:
            connection.disconnect()
print("\nNetwork testing completed.")
