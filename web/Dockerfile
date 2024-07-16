FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y iproute2


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
COPY ./vpn/vpn_manager.py /app/vpn/vpn_manager.py 

EXPOSE 5000

CMD ["python", "app.py"]
