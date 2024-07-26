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


def get_default_network_ip(container_name, network_name='vpn-network_default'):
    client = docker.from_env()
    
    try:
        container = client.containers.get(container_name)
        network_settings = container.attrs['NetworkSettings']['Networks']
        if network_name in network_settings:
            ip_address = network_settings[network_name]['IPAddress']
            return ip_address
        else:
            return f"Network '{network_name}' not found for container '{container_name}'"
    except docker.errors.NotFound:
        return f"Container '{container_name}' not found"
    except Exception as e:
        return str(e)

# Replace 'vpn-network_web_1' with the name of the container you want to get the IP address for
container_name = 'vpn-network_web_1'
ip_address = get_default_network_ip(container_name)
print(f"IP Address of {container_name}: {ip_address}")


def get_docker_containers():
    """
    We'll get all the containers, including non-running containers. 
    Then we'll return the id, name, and status of each container.
    """
    client = docker.from_env()
    containers = client.containers.list(all=True)
    container_info = []
    for container in containers:
        if container.name !="vpn-network_web_vpn_1":
            container_info.append([
                container.short_id,
                container.name,
                container.status,
                container.attrs['NetworkSettings']['IPAddress']
            ])
    return container_info

def get_vpn_status(vpn_container_name):
    client = docker.from_env()
    
    try:
        container = client.containers.get(vpn_container_name)
        # Execute the command to check VPN status inside the container
        exec_log = container.exec_run('pgrep -f openvpn', stdout=True, stderr=True)
        
        if exec_log.exit_code == 0:
            return "Running"
        else:
            return "Stopped"
    except docker.errors.NotFound:
        return f"Container '{vpn_container_name}' not found"
    except Exception as e:
        print(f"Error with VPN: {str(e)}")
        return f"Stopped"
    

    
print(get_docker_containers())

container_name = 'vpn-network_web_1'
ip_address = get_default_network_ip(container_name)
print(f"IP Address of {container_name}: {ip_address}")

vpn_container_name = 'vpn-network_vpn_1'
vpn_status = get_vpn_status(vpn_container_name)
print(vpn_status)