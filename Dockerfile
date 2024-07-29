# Base image
FROM python:3.8-slim

# Install jq
RUN apt-get update && \
    apt-get install -y jq openvpn && \
    apt-get clean

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . /app

# Ensure the entrypoint script has execute permissions
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 5000

# Entrypoint
ENTRYPOINT ["app/entrypoint.sh"]
