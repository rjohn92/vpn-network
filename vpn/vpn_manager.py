import os
import subprocess

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


def get_ip_address():
    # Use a subprocess to run the `ip addr` command and extract the IP address
    result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
    output = result.stdout

    # Extract the IP address from the output
    lines = output.split('\n')
    for line in lines:
        if 'inet ' in line and 'eth0' in line:  # Change 'eth0' to the appropriate interface name
            ip_address = line.split()[1].split('/')[0]
            return ip_address
    return "Couldn't find"