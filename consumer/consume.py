from confluent_kafka import Consumer
import requests

HOST = "broker:29092"
# HOST = "localhost:9092"
TOPIC_NAME = "new_csv_kafka_topic"
################
c = Consumer(
    {
        "bootstrap.servers": HOST,
        "group.id": "python-consumer",
        # "auto.offset.reset": "earliest",
    }
)
print("Kafka Consumer has been initiated...")
print("Available topics to consume: ", c.list_topics().topics)
c.subscribe([TOPIC_NAME])


def main():
    while True:
        msg = c.poll(1.0)  # timeout
        if msg is None:
            continue
        if msg.error():
            print("Error: {}".format(msg.error()))
            continue
        data = msg.value().decode("utf-8")
        x = requests.get(f"http://localhost:8000/csv/{data}")
        print(x.status_code)
        print(data)


main()
