FROM python

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "sunnyportal-to-mqtt.py" ]
