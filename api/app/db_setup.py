from pymongo import MongoClient

import motor.motor_asyncio


host = "mongodb"
conn = MongoClient("mongodb://" + host + ":27017/iot_db")

MONGODB_URL = "mongodb://" + host + ":27017/iot_db"
DATABASE_NAME = "iot_db"
print("MONGODB_URL", MONGODB_URL)


class Database:
    def __init__(self) -> None:
        self.connected = False
        self.mongodb_client = None

    async def db_connection(self):
        if self.connected == False:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

            self.connected = True
        db = self.client[DATABASE_NAME]
        await db["machines"].create_index("unique_identifier", unique=True)
        return db


database = Database()

# import pyspark
# from pyspark import SparkContext, SparkConf
# from pyspark.sql import SparkSession, SQLContext, functions as F
# from pyspark.sql.functions import *


# # create a spark session
# spark = SparkSession \
#     .builder \
#     .master("local") \
#     .appName("ABC") \
#     .config("spark.driver.memory", "15g") \
#     .config("spark.mongodb.read.connection.uri", "mongodb://mongodb:27017/iot_db") \
#     .config("spark.mongodb.write.connection.uri", "mongodb://mongodb:27017/iot_db") \
#     .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector:10.0.2') \
#     .getOrCreate()

# # read data from mongodb collection "questions" into a dataframe "df"
# df = spark.read \
#     .format("mongodb") \
#     .option("uri", "mongodb://mongodb:27017/iot_db") \
#     .option("database", "iot_db") \
#     .option("collection", "machines") \
#     .load()
# df.printSchema()
