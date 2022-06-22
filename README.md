# chatapp-stats-kafka
A simple websocket based chat application.
Use Kafka and KSqlDB to collect chat statistics.

I created this small application just for purpose of learning Confluent Kafka.
Various scripts are adapted from https://github.com/shinichi-hashitani/splunk-confluent-sandbox

### How to run (For future self)
I dockerized this application. To run the app

```bash
docker compose up
```

To build the application docker

```bash
docker build .
```
