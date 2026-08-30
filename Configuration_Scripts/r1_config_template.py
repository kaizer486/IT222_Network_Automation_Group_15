from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
# Enter the connection details of the router you want to configure.
# Use the current GNS3 VM/server IP address and the TELNET console
# port assigned to that router in GNS3.
router = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.92.128",       # Replace with the current GNS3 VM/server IP address
    "username": "",               # Enter username only if required
    "password": "",               # Enter password only if required
    "secret": "",                 # Enter enable password only if required
    "port": 5016,        # Replace with this+-- router's GNS3 TELNET console port
}
# Start the router in GNS3 before running this script.
# Enter the Cisco IOS commands required to configure the router
# according to the provided network topology and addressing information.
commands = [
    "hostname R1",
    "interface GigabitEthernet0/0",
    "no shutdown",
    "interface GigabitEthernet0/0.61",
    "encapsulation dot1Q 61",
    "ip address 192.168.61.1 255.255.255.0",
    "interface GigabitEthernet0/0.71",
    "encapsulation dot1Q 71",
    "ip address 192.168.71.1 255.255.255.0",
    "interface GigabitEthernet0/1",
    "ip address 10.16.16.1 255.255.255.252",
    "no shutdown",
    "router ospf 1",
    "network 192.168.61.0 0.0.0.255 area 0",
    "network 192.168.71.0 0.0.0.255 area 0",
    "network 10.16.16.0 0.0.0.3 area 0",
]
# Create a variable that will store the router connection after
# Netmiko successfully connects to the device.
connection = None
try:
    # Establish a TELNET console connection to the router using
    # the GNS3 VM/server IP address and console port entered above.
    connection = ConnectHandler(**router)
    # Enter privileged EXEC mode if an enable password was supplied.
    if router["secret"]:
        connection.enable()
    # Send all Cisco IOS configuration commands listed in commands.
    output = connection.send_config_set(commands)
    print(output)
    # Enter the show command that should be used to verify
    # that the required network configuration was applied correctly.
    verification = connection.send_command(
        "show ip interface brief"
    )
    print("\n--- Verification ---")
    print(verification)
    # Refresh the base prompt after the hostname change.
    connection.set_base_prompt()
    # Save the completed router configuration.
    connection.save_config()
    print("\nConfiguration completed successfully.")
# Handle cases where Netmiko cannot reach the GNS3 console.
except NetmikoTimeoutException:
    print(
        "Connection timed out. Check the GNS3 VM IP address, "
        "TELNET console port, GNS3 VM, and router state."
    )
# Handle cases where the supplied login or enable credentials are incorrect.
except NetmikoAuthenticationException:
    print(
        "Authentication failed. Check the username, password, "
        "and enable password."
    )
# Display any other error that occurs while running the program.
except Exception as error:
    print(f"Unexpected error: {error}")
finally:
    # Close the TELNET session if a connection was successfully opened.
    if connection is not None:
        connection.disconnect()
