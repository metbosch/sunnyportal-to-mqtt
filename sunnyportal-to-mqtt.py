#!/usr/bin/env python3

from datetime import date, datetime, timedelta
from paho.mqtt import client as mqtt_client

import argparse
import sunnyportal.client, sunnyportal.responses
import json
import time

def main():
  with open("config.json", 'r') as config_file:
    config = json.load(config_file)
    client_mqtt = mqtt_client.Client()
    client_mqtt.username_pw_set(config['mqtt']['username'], config['mqtt']['password'])
    client_mqtt.connect(config['mqtt']['host'], config['mqtt']['port'])
    client_sp = sunnyportal.client.Client(config['sunnyportal']['email'], config['sunnyportal']['password'])
    while True:
      try:
        for plant in client_sp.get_plants():
          data = plant.last_data_exact(date.today() + timedelta(days=1))
          print(f"Total production accumulated:\n  plant={plant.name}\n  wh={data.hour.absolute}")
          client_mqtt.publish(config['mqtt']['topic'], data.hour.absolute)
      except Exception as e:
        print("An exception happened: " + e)
        exit(1)
      time.sleep(300)

if __name__ == "__main__":
  main()
