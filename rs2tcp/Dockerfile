FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "src/python/ttyApi.py", "--ttyDev", "/dev/ttyACM0", "--httpPort", "8080", "--mqttHost", "192.168.4.1", "--mqttPort", "1883", "--mqttTopic", "test" ]

