import os
import subprocess

import docker

def vpn_list():
    config_dir = './vpn/config'  # This path should match the volume mapping in docker-compose.yml
    ovpn_configs = os.listdir(config_dir)
    ovpn_list = [f for f in ovpn_configs if f.endswith(".ovpn")]
    ovpn_list.sort()
    ovpn_list.insert(0, "----Select VPN Location----")
    return ovpn_list


def vpn_providers():
    providers = ["Surfshark", 
    "NordVPN", 
    "ExpressVPN", 
    "CyberGhost", 
    "PIA (Private Internet Access)",
    "VyprVPN", 
    "Mullvad", 
    "ProtonVPN", 
    "IPVanish", 
    "TorGuard", 
    "AirVPN", 
    "Hide.me", 
    "StrongVPN"]
    providers.sort()
    providers.insert(0, "----Select VPN Provider----")
    return providers


import subprocess

def get_ip_address():
    # Use subprocess to get the default route interface
    result = subprocess.run(['ip', 'route', 'get', '8.8.8.8'], capture_output=True, text=True)
    output = result.stdout

    # Extract the interface name from the output
    interface = None
    for line in output.split('\n'):
        if 'dev' in line:
            interface = line.split('dev')[1].split()[0]
            break

    if not interface:
        return "Couldn't find the default route interface"

    # Use subprocess to get the IP address of the identified interface
    result = subprocess.run(['ip', 'addr', 'show', 'dev', interface], capture_output=True, text=True)
    output = result.stdout

    # Extract the IP address from the output
    for line in output.split('\n'):
        if 'inet ' in line:
            ip_address = line.split()[1].split('/')[0]
            return ip_address

    return "Couldn't find the IP address"



def get_docker_containers():
    client = docker.from_env()
    containers = client.containers.list()
    container_info = []
    for container in containers:
        container_info.append([
            container.short_id,
            container.name,
            container.status
        ])
    return container_info


print(get_ip_address())