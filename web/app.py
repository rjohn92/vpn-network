import json
from flask import Flask, request, render_template, jsonify
import os
import sys
from vpn.vpn_manager import vpn_list, vpn_providers, get_ip_address

app = Flask(__name__)

CONFIG_FILE_PATH = '/app/vpn/config/vpn_config.json'

@app.route('/')
def index():
    #generate the list of ovpn files and providers
    ovpn_files=vpn_list()
    ovpn_providers=vpn_providers()
    ip_address = get_ip_address()
    return render_template('index.html', ovpn_files=ovpn_files, 
                           ovpn_providers=ovpn_providers,
                           ip_address=ip_address
                           )

@app.route('/update-credentials', methods=['POST'])
def update_credentials():
    try:
        data = request.get_json()
        ovpn_provider=data.get('ovpn_provider')
        username = data.get('username')
        password = data.get('password')
        ovpn_file = data.get('ovpn_file')

        #check if we have all the fields
        if not ovpn_provider or not username or not password or not ovpn_file:
            raise ValueError("Missing required fields")
        
        config_data = {
            'OVPN_PROVIDER': ovpn_provider,
            'USERNAME': username,
            'PASSWORD': password,
            'OVPN_FILE': ovpn_file
        }


         # Write the configuration to a file
        with open(CONFIG_FILE_PATH, 'w') as config_file:
            json.dump(config_data, config_file)

        return jsonify({"Status": "Credentials updated successfully!"})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"Status: Failed to update credentials!", "Error: {e}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)