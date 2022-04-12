Sunnyportal to MQTT
===================

Service to retrieve solar production from sunnyportal and forward the information to MQTT server.

This project is based on @erijo work: [sunnyportal-py](https://github.com/erijo/sunnyportal-py).
In fact, the library files are a copy of their work.
This project just adds a new main script which periodically polls the website.

## Configuration

This is an under-development work, so the configuration options may change at any point.
See `config.json` file to check the available options.
They should be self descriptive.

## Exported data

The service periodically (random time in `(period.min, period.max)`) publishes a MQTT message to `mqtt.topic` topic.
The message contains a JSON with the following information:

 - plant. Name of plant retrieved from sunnyportal.
 - prod_wh. Solar energy production counter since plant installation.

## Docker

The service can be run using Docker.
The image can be found at [Docker HUB](https://hub.docker.com/r/metbosch/sunnyportal-to-mqtt).
Example to run the image with a custom config file (`home.config.json`):

```
docker run -it --rm --net host -v home.config.json:/usr/src/app/config.json metbosch/sunnyportal-to-mqtt
```
