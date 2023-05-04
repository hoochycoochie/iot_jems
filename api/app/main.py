import datetime
from fastapi import FastAPI, File
import csv
from collections import defaultdict


from app.db_setup import database

# from db_setup import database

app = FastAPI()


# @app.get("/")
# async def read_root():

#     db = await database.db_connection()

#     data = {
#         "machine_id": "1",
#         "createdAt": datetime.datetime.now(),
#         "updatedAt": datetime.datetime.now(),
#         "dateHour": datetime.datetime(2022, 12, 28, 23, 55, 59, 342380),
#         "gpsSpeed": 8.620000000000001,
#         "gpsSatCount": 94.0,
#         "Gear": 131.0,
#         "Brake_pedal": 131.0,
#         "Accel_pedal": 0.0,
#         "Machine_Speed_Mesured": 20.0,
#         "AST_Direction": 20.0,
#         "Ast_HPMB1_Pressure_bar": 0.0,
#         "Ast_HPMA_Pressure_bar": 0.0,
#         "Pressure_HighPressureReturn": 0.0,
#         "Pressure_HighPressure": 32826.0,
#         "Oil_Temperature": 58.0,
#         "Ast_FrontAxleSpeed_Rpm": 32826.0,
#         "Pump_Speed": 894.0,
#     }

#     # print("db.machines", db.machines)
#     data_encoded = jsonable_encoder(data)
#     # print("data_encoded", data_encoded)
#     result = await db.machines.insert_one(data_encoded)
#     # print("result", result)
#     machines = await db.machines.find().to_list(length=90)
#     print("machines", machines)

#     return {"machines": "machines"}


def custom_date(string_date):
    [year_month, hours] = string_date.split(" ")
    [year, month, day] = year_month.split("-")
    [hh, mn, second] = hours.split(":")
    [ss, micross] = second.split(".")
    year = int(year)
    month = int(month)
    day = int(day)
    hh = int(hh)
    mn = int(mn)
    ss = int(ss)
    micross = int(micross)
    return datetime.datetime(year, month, day, hh, mn, ss, micross)


@app.get("/csv/{file_id}")
def read_root(file_id: str):

    filename = "../../producer/csv_data/" + file_id
    print("c", filename)

    return {"item_id": file_id}


@app.post("/csv/")
async def create_upload_file(filename: str, file: bytes = File(...)):
    try:
        [machine_id, date_csv] = filename.split("_")
        lines = file.decode("utf-8").splitlines()
        headers = lines[0].split(";")
        headers_to_parse = [col for col in headers if col not in ["dateHour"]]

        reader = csv.DictReader(lines, delimiter=";")
        lst = list(reader)
        dst = dict(enumerate(lst))
        db = await database.db_connection()

        for _, value in dst.items():
            for key, val in value.items():
                if key in headers_to_parse:
                    value[key] = float(val)
            value["createdAt"] = datetime.datetime.now()
            value["updatedAt"] = datetime.datetime.now()
            value["machine_id"] = machine_id
            # unique_identifier
            value["unique_identifier"] = filename + value["dateHour"]
            value["dateHour"] = custom_date(value["dateHour"])
            await db.machines.insert_one(value)

        return {
            "success": True,
        }
    except Exception as error:
        print("error", error)
        # return HTTPException(500, error._message)
        return error._message
