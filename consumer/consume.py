from confluent_kafka import Consumer
from influxdb import InfluxDBClient
import pandas as pd


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
# influx_host = "localhost"
client = InfluxDBClient(host=influx_host, port=8086)
client.switch_database("iot_db")

from os.path import abspath, isfile


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
        print("data", data)
        path = abspath("./csv_data/" + data)
        print("path", path)
        if isfile(path):
            df = pd.read_csv(path, sep=";")
            print("len(df) =========", len(df))
            if len(df) > 0:
                payload = []
                for _, row in df.iterrows():

                    tb = {
                        "measurement": "iot",
                        "tags": {"machine_id": row["product_name"]},
                        "time": row["dateHour"],
                        "fields": {
                            "product_name": "dateHour",
                            "product_category": row["product_category"],
                            "dateHour": row["dateHour"],
                            "gpsSpeed": row["gpsSpeed"],
                            "gpsSatCount": row["gpsSatCount"],
                            "Gear": row["Gear"],
                            "Brake_pedal": row["Brake_pedal"],
                            "Accel_pedal": row["Accel_pedal"],
                            "Machine_Speed_Mesured": row["Machine_Speed_Mesured"],
                            "AST_Direction": row["AST_Direction"],
                            "Ast_HPMB1_Pressure_bar": row["Ast_HPMB1_Pressure_bar"],
                            "Ast_HPMA_Pressure_bar": row["Ast_HPMA_Pressure_bar"],
                            "Pressure_HighPressureReturn": row[
                                "Pressure_HighPressureReturn"
                            ],
                            "Pressure_HighPressure": row["Pressure_HighPressure"],
                            "Oil_Temperature": row["Oil_Temperature"],
                            # "Ast_FrontAxl": row["Ast_FrontAxl"],
                        },
                    }
                    payload.append(tb)

                    # print(df.head())
                    print("payload", payload)

                    result = client.write_points(payload)
                    print("result", result)
                    print("new data", data)


main()
