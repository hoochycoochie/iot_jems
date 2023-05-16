import csv
import random
from datetime import datetime
import pytz
from threading import Timer
from confluent_kafka import Producer
import logging

# from snakebite.client import Client

# HADOOP_HOST = "localhost"
# # HADOOP_HOST='namenode'
# client = Client(HADOOP_HOST, 9000)

# for p in client.mkdir(["/demo/demo1", "/demo2"], create_parent=True):
#     print("p", p)


HOST = "broker:29092"
# HOST = "localhost:9092"
logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="producer.log",
    filemode="w",
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def receipt(err, msg):
    if err is not None:
        print("Error: {}".format(err))
    else:
        message = "Produced message on topic {} with value of {}\n".format(
            msg.topic(), msg.value().decode("utf-8")
        )
        logger.info(message)
        print(message)


machines = [
    {"machine_id": 1, "product_name": "peugeot 208", "product_category": "vehicule"},
    {"machine_id": 2, "product_name": "clio 4", "product_category": "vehicule"},
]
period = 5
fields = [
    "product_name",
    "product_category",
    "dateHour",
    "gpsSpeed",
    "gpsSatCount",
    "Gear",
    "Brake_pedal",
    "Accel_pedal",
    "Machine_Speed_Mesured",
    "AST_Direction",
    "Ast_HPMB1_Pressure_bar",
    "Ast_HPMA_Pressure_bar",
    "Pressure_HighPressureReturn",
    "Pressure_HighPressure",
    "Oil_Temperature",
    "Ast_FrontAxleSpeed_Rpm",
    "Pump_Speed",
]


def gen_csv():
    Timer(period, gen_csv).start()
    now = datetime.now()

    # second = str(now.second)
    minute = str(now.minute)
    hour = str(now.hour)

    day = str(now.day)
    month = str(now.month)
    year = str(now.year)
    date_time = year + "-" + month + "-" + day + " " + hour + ":" + minute
    machine = random.choice(machines)

    machine_id = str(machine["machine_id"])
    product_name = machine["product_name"]
    product_category = machine["product_category"]
    print("machine_id", machine_id)
    print("product_name", product_name)
    print("product_category", product_category)
    rows = [
        [
            product_name,
            product_category,
            date_time
            + ":0."
            + str(datetime.now().microsecond),  # "2018-01-19 05:37:0.612611",
            random.uniform(5, 8.62),  #  8.62,
            random.randint(50, 94),  # 94,
            random.randint(0, 131),  # 131,
            random.randint(0, 131),  # 131,
            random.randint(0, 1),  #  0,
            random.randint(10, 20),  #  20,
            random.randint(10, 20),  #  20,
            random.randint(0, 1),  #  0,
            random.randint(0, 1),  #  0,
            random.randint(0, 1),  #  0,
            random.randint(12345, 32826),  #     32826,
            random.randint(38, 58),  #      58,
            random.randint(12345, 32826),  #     32826,
            random.randint(128, 894),  #    894,
        ],
    ]

    newYorkTz = pytz.timezone("Europe/Paris")
    timeInNewYork = str(datetime.now(newYorkTz))

    # name of csv file
    csv_file = "X467" + machine_id + "_" + timeInNewYork + ".csv"
    filename = "./csv_data/" + csv_file

    # writing to csv file
    with open(filename, "w") as csvfile:
        # creating a csv writer object
        try:
            csvwriter = csv.writer(csvfile, delimiter=";")

            # writing the fields
            csvwriter.writerow(fields)

            # writing the data rows
            csvwriter.writerows(rows)
            # client.copyFromLocal(csv_file, "/csv_data/" + csv_file)
            TOPIC_NAME = "new_csv_kafka_topic"
            p = Producer({"bootstrap.servers": HOST})

            p.produce(TOPIC_NAME, csv_file, callback=receipt)
            p.flush()
        except Exception as e:
            print("error", e)
        # logger.log(e).debug()
        finally:
            # if os.path.exists(filename):
            #     os.remove(filename)
            #     print("file removed", filename)
            print("ok finally")


gen_csv()
