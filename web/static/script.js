document.addEventListener('DOMContentLoaded', function() {
    // This function runs when the DOM content is fully loaded

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

            console.log("Data",data)
            try {
                const response = await fetch('/update-credentials', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                console.log(response)
                const result = await response.json();
                console.log(result)
                document.getElementById('status').innerText = result.Status;
            } catch (error) {
                console.error(JSON.stringify(error));
                document.getElementById('status').innerText = 'Error updating credentials!';
            }
        });
    } else {
        console.error('Credentials form not found!');
    }
});
