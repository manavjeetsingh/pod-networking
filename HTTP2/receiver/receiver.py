import numpy as np
from fastapi import FastAPI, Request
import time
import logging
import pickle
# Why use FastAPI app?
app = FastAPI()
first_time_sent=None
last_time_sent=None
first_time_got=None
last_time_got=None
flow=None
delay=0
@app.get("/ping")
def ping():
    return {"status": "Success"}




@app.post("/rec")
async def receive_packets(request: Request):
    global first_time_got
    global first_time_sent
    global last_time_got
    global last_time_sent
    global flow
    global delay
    data_in_bytes: bytes = await request.body()
    current_time=time.time()
    data=pickle.loads(data_in_bytes)
    packet_no=data[0]
    if data[3]!=flow:
        flow=data[3]
        first_time_got=current_time
        first_time_sent=data[1]
        delay=0
    last_time_got=current_time
    last_time_sent=data[1]
    # logging.info("Recieved packet with a delay of: "+str(current_time-data[1]))
    delay+=last_time_got - last_time_sent
    # logging.info("Delay in flow number "+  str(flow)+" Id: " + str(first_time_sent-last_time_got))
    logging.info("Avg Delay in flow number "+  str(flow)+" Id: " + str(packet_no)+" is :" + str(delay/(packet_no+1)))
    # logging.info("Received data of size:"+str(len(data_in_bytes)))
    # return "got"