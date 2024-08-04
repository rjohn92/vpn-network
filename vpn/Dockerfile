# Use a base image that supports OpenVPN
FROM ubuntu:latest

# Install OpenVPN
RUN apt-get update && \
    apt-get install -y openvpn iptables\
    apt-clean

# Copy VPN configuration files into the container
COPY entrypoint.sh /usr/local/bin/

# Make the script executable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
