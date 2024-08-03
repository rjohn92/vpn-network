import logging
from flask import Flask, request, render_template, jsonify
import os
import vpn.vpn_manager

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONFIG_FILE_PATH = '/app/vpn/config'
NETWORK_NAME = os.getenv('NETWORK_NAME', 'vpn_network')


@app.route('/')
def index():
    #generate the list of ovpn files and providers
    return render_template('index.html', ovpn_files=vpn.vpn_manager.vpn_list(), 
                           ovpn_providers=vpn.vpn_manager.vpn_providers(),
                           status=vpn.vpn_manager.get_vpn_status("vpn_container"),
                           docker_containers=vpn.vpn_manager.get_docker_containers()
                           )

@app.route('/update-credentials', methods=['POST'])
def update_credentials():

    try:
        #get the data form from the web page
        data = request.get_json()
        ovpn_provider=data.get('ovpn_provider')
        username = data.get('username')
        password = data.get('password')
        ovpn_file = data.get('ovpn_file')


        #Create the network we will attach our vpn container to
        vpn.vpn_manager.create_network("private_network")

        #start the vpn first to get the service running
        status_message, status_code = vpn.vpn_manager.start_vpn(ovpn_provider,ovpn_file, username, password)
        
        return jsonify(status_message), status_code
    
    except Exception as e:
        print(f"Error: {e}")
        vpn.vpn_manager.remove_network("private_network")
        return jsonify({"Status": f"Failed to update credentials: {str(e)}"}), 500
   
@app.route('/stop-vpn', methods=['POST'])
def stop_vpn():
    try:
        response, status_code = vpn.vpn_manager.stop_container()
        return response, status_code
    except Exception as e:
        return jsonify({"Status": "Failed to stop VPN container!"})
    
app.route('/vpn-logs', methods = ['GET'])
def vpn_logs():
    logs = vpn.vpn_manager.get_vpn_logs()
    if logs:
        return jsonify({"Logs": logs}), 200
    else:
        return jsonify({"Status": "Failed to retrieve VPN logs"}), 500