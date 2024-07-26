#!/bin/bash

# Start the Flask app
gunicorn --bind 0.0.0.0:5000 web.app:app &

# Wait for Flask app to start
sleep 5

# Check and wait for the configuration file
while true; do
  if [ -f "${CONFIG_FILE_PATH}" ]; then
    echo "Configuration file found: ${CONFIG_FILE_PATH}"
    break
  else
    echo "Waiting for configuration file..."
    sleep 5
  fi
done

# Read the configuration file and extract variables using jq
OVPN_PROVIDER=$(jq -r '.ovpn_provider' "${CONFIG_FILE_PATH}")
USERNAME=$(jq -r '.username' "${CONFIG_FILE_PATH}")
PASSWORD=$(jq -r '.password' "${CONFIG_FILE_PATH}")
OVPN_FILE=$(jq -r '.ovpn_file' "${CONFIG_FILE_PATH}")

# Print the variables
echo "OVPN_PROVIDER: ${OVPN_PROVIDER}"
echo "USERNAME: ${USERNAME}"
echo "PASSWORD: ${PASSWORD}"
echo "OVPN_FILE: ${OVPN_FILE}"

# Proceed with OpenVPN configuration and start the VPN
if [ -n "${OVPN_FILE}" ] && [ -f "/etc/openvpn/config/${OVPN_FILE}" ]; then
  echo "Starting OpenVPN with file: /etc/openvpn/config/${OVPN_FILE}"
  openvpn --config "/etc/openvpn/config/${OVPN_FILE}"
else
  echo "OpenVPN configuration file not found: /etc/openvpn/config/${OVPN_FILE}"
fi