import os
import subprocess
import tempfile
import docker
import logging

from flask import jsonify

#config files in the docker container
CONFIG_FILE_PATH = "/app/vpn/config/"
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

network_logs = "/tmp/network.log"
openvpn_logs = "/tmp/openvpn.log"

#set the docker client
client = docker.from_env()

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

def get_docker_containers():
    """
    We'll get all the containers, including non-running containers. 
    Then we'll return the id, name, and status of each container.
    """
    containers = client.containers.list(all=True)
    container_info = []
    for container in containers:
        if container.name !="vpn-network_web_vpn_1":
            container_info.append([
                container.short_id,
                container.name,
                container.status,
                get_container_ip(container.name)
            ])
    return container_info

def get_vpn_status(vpn_container_name):
    
    try:
        container = client.containers.get(vpn_container_name)
        # Execute the command to check VPN status inside the container
        status = container.status 
        
        if status  == "running":
            return "Running"
        elif status== "exited":
            return "Stopped"
    except docker.errors.NotFound:
        return f"Container '{vpn_container_name}' not found"
    except Exception as e:
        print(f"Error with VPN: {str(e)}")
        return f"Stopped"
    

def get_container_ip(container_name):


    try:
        # Get the container object
        container = client.containers.get(container_name)
        
        # Retrieve network settings
        network_settings = container.attrs.get('NetworkSettings')
        networks = network_settings.get('Networks')
        
        # Extract IP addresses from all networks
        ip_addresses = [network.get('IPAddress') for network in networks.values()]
        
        # Concatenate IP addresses into a single string
        ip_address_string = ''.join(ip_addresses) if ip_addresses else 'No IP address found'
        
        return ip_address_string
    except docker.errors.NotFound:
        print(f"Container '{container_name}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
        
def create_network(network_name):
    try:
        network = client.networks.create(network_name)
        logger.info(f"Network created successfully: {network.name}")
    except Exception as e:
        logger.error(f"Failed to generate network: {e}")
        

def remove_network(network_name):
    try:
        network = client.networks.get(network_name)
        network.remove()
        logger.info(f"Network: {network_name} removed")
    except:
        logger.info(f"Network: {network_name} could not be removed")


def start_vpn(ovpn_provider, ovpn_file, username, password):
    if not ovpn_provider or not username or not password or not ovpn_file:
        return {"Status": "Missing required fields!"}, 400

    if ovpn_provider == "----Select VPN Provider----":
        return {"Status": "You must select an OVPN Provider!"},400

    if ovpn_file == "----Select VPN Location----":
        return {"Status": "You must select an OVPN File!"}, 400


    # Save files temporarily
    ovpn_file_path, auth_file_path = save_user_files(ovpn_file, username, password)

    # Start VPN container
    container = start_vpn_container(ovpn_file_path, auth_file_path)
    print(container)
    if container:
        return {"Status": "VPN container started successfully!"}, 200
    else:
        return {"Status": "Failed to start VPN container!"}, 500


def save_user_files(ovpn_file_content, username, password):
    # Save the .ovpn file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ovpn") as ovpn_file:
        ovpn_file.write(ovpn_file_content.encode())
        ovpn_file_path = ovpn_file.name

    # Save the credentials
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as auth_file:
        auth_file.write(f"{username}\n{password}".encode())
        auth_file_path = auth_file.name

    return ovpn_file_path, auth_file_path


def start_vpn_container(ovpn_file_path, auth_file_path,container_name="vpn_container"):
    remove_container(container_name)
    try:
        build_image()
        container = client.containers.run(
            "custom_vpn_client",
            name=container_name,
            network="private_network",
            volumes={
                ovpn_file_path: {'bind': '/etc/openvpn/config.ovpn', 'mode': 'ro'},
                auth_file_path: {'bind': '/etc/openvpn/auth.txt', 'mode': 'ro'}
            },
            detach=True
        )
        return container
        
    except docker.errors.APIError as e:
        print(f"Failed to start VPN container: {e}")
        return None

def stop_container(container_name="vpn_container"):
    try:
        container = client.containers.get(container_name)
        container.stop()
        logger.info(f"Stopped VPN container: {container_name}")
        return {f"Status": "VPN container stopped successfully!"}, 200
    except Exception as e:
        logger.error(f"Failed to stop VPN container: {e}")
        return {"Status": "Failed to stop VPN container!"}, 500

def build_image():
    try:
        image_name = "custom_vpn_client"
        dockerfile_path = "vpn"  # Adjust this path

        logger.info(f"Building Docker image: {image_name}")
        
        # Build the image
        client.images.build(path=dockerfile_path, tag=image_name)
        
        logger.info(f"Successfully built Docker image: {image_name}")
    except docker.errors.BuildError as e:
        logger.error(f"Failed to build Docker image: {e}")
        raise
    except docker.errors.APIError as e:
        logger.error(f"Docker API error: {e}")
        raise

def remove_container(container_name):
    try: 
        container = client.containers.get(container_name)
        container.remove(force=True)
        logger.info(f"Successfully removed container: {container_name}")
    except docker.errors.NotFound:
        logger.info(f"Container {container_name} not found")
    except docker.errors.APIError as e:
        logger.error(f"Failed to remove container: {e}")


def get_vpn_logs(container_name="vpn_container"):
    try:
        container = client.containers.get(container_name)
        logs = container.logs(tail=100).decode('utf-8')  # Get the last 100 lines of logs
        return logs
    except docker.errors.NotFound:
        logger.error(f"Container {container_name} not found. Cannot retrieve logs.")
        return None
    except docker.errors.APIError as e:
        logger.error(f"Failed to get logs for container {container_name}: {e}")
        return None