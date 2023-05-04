import datetime
from pydantic import BaseModel
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):

        yield cls.validate

    @classmethod
    def validate(cls, v):

        if not ObjectId.is_valid(v):

            raise ValueError("Invalid objectid")

        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):

        field_schema.update(type="string")


class Machine(BaseModel):
    # id: str = Field(default_factory=uuid.uuid4, alias="_id")
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    # timestamp: datetime.datetime = datetime.datetime.now()
    unique_identifier = str
    createdAt: datetime = datetime.datetime.now()
    updatedAt: datetime = datetime.datetime.now()
    machine_id: str
    dateHour: datetime.datetime
    gpsSpeed: float
    gpsSatCount: float
    Gear: float
    Brake_pedal: float

    Accel_pedal: float
    Machine_Speed_Mesured: float
    AST_Direction: float
    Ast_HPMB1_Pressure_bar: float
    Ast_HPMA_Pressure_bar: float
    Pressure_HighPressureReturn: float
    Pressure_HighPressure: float
    Oil_Temperature: float
    Ast_FrontAxleSpeed_Rpm: float
    Pump_Speed: float

    class Config:
        orm_mode = True
        timestamps = True
        allow_population_by_field_name = True

        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

        # schema_extra = {
        #     "example": {
        #         "name": "Jane Doe",
        #         "email": "jdoe@example.com",
        #         "course": "Experiments, Science, and Fashion in Nanophotonics",
        #         "gpa": "3.0",
        #     }
        # }
