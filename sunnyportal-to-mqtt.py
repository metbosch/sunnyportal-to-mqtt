#!/usr/bin/env python3

from datetime import date, datetime, timedelta
from paho.mqtt import client as mqtt_client

import argparse
import sunnyportal.client, sunnyportal.responses
import json
import random
import time

def main():
  print(f"{datetime.now()}: Starting sunnyportal-to-mqtt")
  with open("config.json", 'r') as config_file:
    config = json.load(config_file)
    client_mqtt = mqtt_client.Client()
    client_mqtt.username_pw_set(config['mqtt']['username'], config['mqtt']['password'])
    client_mqtt.connect(config['mqtt']['host'], port=config['mqtt']['port'], keepalive=config['mqtt']['keepalive'])
    while True:
      print(f"{datetime.now()}: Starting sunnyportal information retrievement")
      try:
        client_sp = sunnyportal.client.Client(config['sunnyportal']['email'], config['sunnyportal']['password'])
        for plant in client_sp.get_plants():
          data = plant.last_data_exact(date.today() + timedelta(days=1))
          wh = data.hour.absolute if not data.hour is None else None
          print(f"{datetime.now()}: wh={wh} plant={plant.name}")
          if not wh is None:
            data_mqtt = '{"plant": "' + plant.name + '", "prod_wh": ' + str(wh) + '}'
            (mqtt_err, mqtt_mid) = client_mqtt.publish(config['mqtt']['topic'], data_mqtt)
            if mqtt_err != 0:
              print(f"{datetime.now()}: MQTT publish failed:  {str(mqtt_err)}, {config['mqtt']['topic']}, {data_mqtt}")
      except Exception as e:
        print(f"{datetime.now()}: Exception:  {str(e)}")
        exit(1)
      seconds_delay = random.randrange(config['period']['min'], config['period']['max'])
      time.sleep(seconds_delay)

main()
