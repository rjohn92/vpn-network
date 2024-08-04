document.addEventListener('DOMContentLoaded', function() {
    // This function runs when the DOM content is fully loaded

    // Function to determine status class
    function statusClass(status) {
        if (status === 'running' || status === 'Running') {
            return 'status-running';
        } else if (status === 'exited' || status.includes("Stopped") ) {
            return 'status-stopped';
        } else {
            return 'status-other';
        }
    }

    // Add status classes to container rows
    const statusElements = document.querySelectorAll('[data-status]');
    statusElements.forEach(element => {
        const status = element.getAttribute('data-status');
        element.classList.add(statusClass(status));
    });

    // Add event listener to the credentials form
    const credentialsForm = document.getElementById('credentials-form');
    if (credentialsForm) {
        credentialsForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(credentialsForm);
            const data = {
                ovpn_provider: formData.get('ovpn_provider'),
                username: formData.get('username'),
                password: formData.get('password'),
                ovpn_file: formData.get('ovpn_file')
            };

            console.log("Data", data);
            try {
                const response = await fetch('/update-credentials', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                console.log(response);
                const result = await response.json();
                console.log(result);
                document.getElementById('message').innerText = result.Status;
            } catch (error) {
                console.error(JSON.stringify(error));
                document.getElementById('message').innerText = 'Error updating credentials!';
            }
        });        
    }
    // Add event listener to the disconnect button
    const disconnectButton = document.getElementById('disconnectButton');
    if (disconnectButton) {
        disconnectButton.addEventListener('click', async function() {
            try {
                const response = await fetch('/stop-vpn', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                const result = await response.json();
                console.log(result);
                alert(result.Status);
            } catch (error) {
                console.error(JSON.stringify(error));
                alert('Error disconnecting VPN!');
            }
        });   
    }
    const connectButtons = document.querySelectorAll('.connect-btn');
    
    connectButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const containerName = button.getAttribute('data-container'); // Get the container name from the button's data attribute            try {
            try {    
                const response = await fetch('/connect-container', {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ containerName }) // Send container name as JSON

                });
                const result = await response.json();
                console.log(result);
                alert(result.Status)
            } catch (error) {
                console.error(JSON.stringify(error));
                alert('Error connecting Container!');
            }
        });
        });
    });
