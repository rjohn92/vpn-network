# VPN Network Management System

## Prerequisites
- Make sure you have docker install first. If you need to install docker go [here](https://docs.docker.com/engine/install/) and follow the instructions for your respective operating system. 

- Make sure you have an OpenVPN service provider account set up. Follow [this link for instructions](https://www.tp-link.com/us/support/faq/3763/) on how to access your OpenVPN credentials (which are different from your username/email and password account setup)

## Project Overview
The VPN Network Management System is a Flask-based web application designed to create a graphical user interface (GUI) for managing VPN connections using OpenVPN configuration files. The primary goal of this project is to simplify the process of managing VPN connections and integrating them with existing Docker containers on your system.

Some VPN providers allow the user to decide which applications/services they would like to route their internet traffic through. When the user does this it's called [split tunneling](https://www.fortinet.com/resources/cyberglossary/vpn-split-tunneling). This is mostly helpful when you would like to make sure some services use the encrypted network provided by your VPN to help shield yourself from your Internet Service Provider's (ISP) prying eyes while still allowing the traffic you don't mind being visible to your ISP to visible. 

But this service is not always available to all VPN providers. This project is helpful in allowing non-technically inclined people to benefit from split tunneling without necessarily needing to set up their own docker container/VPN from scratch. 

## Features

- **VPN Management**: Create and manage VPN connections using OpenVPN configuration files.
- **Web GUI**: User-friendly interface to enter VPN credentials and manage VPN connections.
- **Integration with Docker**: View all running Docker containers on the system and attach them to the VPN with a single click.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/rjohn92/vpn-network.git
   cd vpn-network

1. Go here:
http://localhost:5000/
