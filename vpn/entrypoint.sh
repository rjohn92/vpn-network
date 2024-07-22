#!/bin/bash


# Read environment variables for credentials and config file
CONFIG_FILE_PATH=${CONFIG_FILE_PATH:-/etc/openvpn/config/vpn_config.json}

if [ ! -f "$CONFIG_FILE_PATH" ]; then
  echo "Configuration file not found: $CONFIG_FILE_PATH"
  exit 1
fi

# Extract credentials and config details from the JSON file
OVPN_PROVIDER=$(jq -r '.OVPN_PROVIDER' "$CONFIG_FILE_PATH")
USERNAME=$(jq -r '.USERNAME' "$CONFIG_FILE_PATH")
PASSWORD=$(jq -r '.PASSWORD' "$CONFIG_FILE_PATH")
OVPN_FILE=$(jq -r '.OVPN_FILE' "$CONFIG_FILE_PATH")

# Let's try to print the extracted variables
echo "OVPN_PROVIDER: $OVPN_PROVIDER"
echo "USERNAME: $USERNAME"
echo "PASSWORD: $PASSWORD"
echo "OVPN_FILE: $OVPN_FILE"

# Ensure the OVPN file exists
if [ ! -f "/etc/openvpn/config/${OVPN_FILE}" ]; then
  echo "OpenVPN configuration file not found: /etc/openvpn/config/${OVPN_FILE}"
  exit 1
fi

#print the variables
#echo -e "${USERNAME}\n${PASSWORD}" > /etc/openvpn/auth.txt


# Start OpenVPN with the provided configuration and credentials
# Use a here document to pass the credentials via stdin
openvpn --config /etc/openvpn/config/${OVPN_FILE} --auth-user-pass <(echo -e "${USERNAME}\n${PASSWORD}")