import numpy as np
from fastapi import FastAPI, Request
import time
import logging
# Why use FastAPI app?
app = FastAPI()


@app.get("/ping")
def ping():
    return {"status": "Success"}


@app.post("/rec")
async def receive_packets(request: Request):
    data_in_bytes: bytes = await request.body()
    logging.info("Received data of size:"+str(len(data_in_bytes)))
    # return "got"