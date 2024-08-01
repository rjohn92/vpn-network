import json
import logging
import subprocess
from celery import Celery
from flask import Flask, request, render_template, jsonify
import os
import sys
from vpn.vpn_manager import start_vpn, get_docker_containers,vpn_list, vpn_providers, get_vpn_status, save_config


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONFIG_FILE_PATH = '/app/vpn/config'
NETWORK_NAME = os.getenv('NETWORK_NAME', 'vpn_network')


@app.route('/')
def index():
    #generate the list of ovpn files and providers
    return render_template('index.html', ovpn_files=vpn_list(), 
                           ovpn_providers=vpn_providers(),
                           status=get_vpn_status("vpn-network_web_vpn_1"),
                           docker_containers=get_docker_containers()
                           )

@app.route('/update-credentials', methods=['POST'])
def update_credentials():
    try:
        data = request.get_json()
        ovpn_provider=data.get('ovpn_provider')
        username = data.get('username')
        password = data.get('password')
        ovpn_file = data.get('ovpn_file')

        if not username or not password or ovpn_file == "----Select VPN Location----" or ovpn_provider == "----Select VPN Provider----" :
            return jsonify({"Status": "Missing required fields!"})

        logger.info(f"Attempting to start VPN in app.py.")


        pid =start_vpn(ovpn_file,username, password)
        if pid:
            return jsonify({"Status": "Credentials are valid! VPN instance started."}), 200
        else:
            return jsonify({"Status": "Failed to start VPN instance! Check your credentials."})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"Status": f"Failed to update credentials!"}), 500
   