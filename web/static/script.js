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
});
