# You need this to use FastAPI, work with statuses and be able to end HTTPExceptions
from fastapi import FastAPI, status, HTTPException

# You need this to be able to turn classes into JSONs and return
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Needed for json.dumps
import json

# Both used for BaseModel
from pydantic import BaseModel

from datetime import datetime
from kafka import KafkaProducer, producer



# Create class (schema) for the JSON
# Date get's ingested as string and then before writing validated
class InvoiceItem(BaseModel):
    Date: str
    Opp: str
    AB: int
    HR: int
    OppStarter: str


# This is important for general execution and the docker later
app = FastAPI()

# Base URL
@app.get("/")
async def root():
    return {"message": "Hello World from my code"}

@app.post("/gamelogitem")
async def post_invoice_item(item: InvoiceItem):
    print("Message received")
    try:

        # Parse item back to json
        json_of_item = jsonable_encoder(item)

        # Dump the json out as string
        json_as_string = json.dumps(json_of_item)
        print(json_as_string)

        # Produce the string
        produce_kafka_string(json_as_string)

        # Encode the created customer item if successful into a JSON and return it to the client with 201
        return JSONResponse(content=json_of_item, status_code=201)

    # Will be thrown by datetime if the date does not fit
    # All other value errors are automatically taken care of because of the InvoiceItem Class
    except ValueError:
        return JSONResponse(content=jsonable_encoder(item), status_code=400)

def produce_kafka_string(json_as_string):
    # Create producer
        producer = KafkaProducer(bootstrap_servers='kafka:9092',acks=1)

        # Write the string as bytes because Kafka needs it this way
        producer.send('ingestion-topic', bytes(json_as_string, 'utf-8'))
        producer.flush()
