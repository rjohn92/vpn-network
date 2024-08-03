#!/bin/bash

# Start the OpenVPN client and redirect output to a log file
openvpn --config /etc/openvpn/config.ovpn --auth-user-pass /etc/openvpn/auth.txt > /tmp/openvpn.log 2>&1

# Keep the container running by tailing the log file
tail -f /tmp/openvpn.log
