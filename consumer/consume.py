from confluent_kafka import Consumer
from influxdb import InfluxDBClient


# import requests

HOST = "broker:29092"
# HOST = "localhost:9092"
TOPIC_NAME = "new_csv_kafka_topic"
################
c = Consumer(
    {
        "bootstrap.servers": HOST,
        "group.id": "python-consumer",
        "session.timeout.ms": 6000,
        "auto.offset.reset": "earliest",
        "enable.auto.offset.store": False,
    }
)
print("c======", c)
print("Kafka Consumer has been initiated...")
print("Available topics to consume: ", c.list_topics().topics)
c.subscribe([TOPIC_NAME])

print("client=======================11111111111111111111&")
influx_host = "influxdb"
client = InfluxDBClient(host=influx_host, port=8086)
client.switch_database("iot_db")
print("client=======================", client)


def main():
    while True:
        msg = c.poll(1.0)  # timeout
        if msg is None:
            continue
        if msg.error():
            print("Error: {}".format(msg.error()))
            continue
        data = msg.value().decode("utf-8")
        # x = requests.get(f"http://localhost:8000/csv/{data}")
        # print(x.status_code)
        print("new data", data)


main()
