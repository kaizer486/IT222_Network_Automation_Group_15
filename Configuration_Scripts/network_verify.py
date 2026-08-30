from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
# Start the required devices in GNS3 before running this script.
# Replace the host address and TELNET console ports with the values
# currently assigned by the student's GNS3 environment.
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
        "name": "R2",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.92.128",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5018,  # Replace with the current R2 TELNET console port.
    },
    {
        "name": "SW1",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.92.128",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5020,  # Replace with the current SW1 TELNET console port.
    },
    {
        "name": "SW2",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.92.128",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5022,  # Replace with the current SW2 TELNET console port.
    },
]
# Use a list of lists so that each device has its own verification commands.
# The first item in each inner list is the device name. The remaining items
# are commands that are applicable to that device and the assigned scenario.
verification_commands = [
    [
        "R1",
        "show ip interface brief",
        "show ip route",
        "show ip ospf neighbor",
    ],
    [
        "R2",
        "show ip interface brief",
        "show ip route",
        "show ip ospf neighbor",
    ],
    [
        "SW1",
        "show vlan brief",
        "show interfaces trunk",
        "show interfaces status",
        "show mac address-table",
    ],
    [
        "SW2",
        "show vlan brief",
        "show interfaces trunk",
        "show interfaces status",
        "show mac address-table",
    ],
]
# Connect to each selected device and run only the verification commands
# assigned to that device.
for device in devices:
    connection = None
    device_name = device["name"]
    # Remove the name field because Netmiko does not use it.
    connection_details = {
        key: value
        for key, value in device.items()
        if key != "name"
    }
    # Find the verification-command list for the current device.
    commands_for_device = []
    for command_group in verification_commands:
        if command_group[0] == device_name:
            commands_for_device = command_group[1:]
            break
    if not commands_for_device:
        print(f"\n{device_name}: No verification commands have been assigned.")
        continue
    try:
        print(f"\nConnecting to {device_name}...")
        connection = ConnectHandler(**connection_details)
        # Enter privileged EXEC mode if an enable password is provided.
        if connection_details["secret"]:
            connection.enable()
        # Disable output paging so long command output is not cut off.
        connection.send_command("terminal length 0")
        for command in commands_for_device:
            print(f"\n--- {device_name}: {command} ---")
            output = connection.send_command(command)
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
print("\nNetwork verification completed.")
