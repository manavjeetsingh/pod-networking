from client import QuicConfiguration,main, main_stripped
import asyncio
from aioquic.h3.connection import H3_ALPN, ErrorCode, H3Connection

import numpy as np
from fastapi import FastAPI, Request
import os
import pickle
import requests
import time


import numpy as np
from fastapi import FastAPI, Request
import os
import pickle
import requests
import time

app = FastAPI()
@app.get("/ping")
def ping():
    return {"status": "Success"}


async def send_packet(size):
    configuration= QuicConfiguration(
            is_client=True, alpn_protocols=H3_ALPN
        )

    configuration.load_verify_locations("pycacert.pem")
    urls=["https://localhost:4433/res"]
    data = os.urandom(size) 

    # asyncio.run(
    await main_stripped(
        configuration=configuration,
        urls=urls,
        data=data,
        include=None,
        output_dir="./",
        local_port=0,
        zero_rtt=True,
    )
    # )


async def send_packet_single_connection(size,packets):
    configuration= QuicConfiguration(
            is_client=True, alpn_protocols=H3_ALPN
        )

    configuration.load_verify_locations("pycacert.pem")
    urls=["https://localhost:4433/res"]
    data = os.urandom(size) 

    # asyncio.run(
    await main_stripped(
        configuration=configuration,
        urls=urls,
        data=data,
        include=None,
        output_dir="./",
        local_port=0,
        zero_rtt=True,
        packets=packets
    )
    # )


# if __name__=="__main__":
#     send_packet(10)

@app.post("/send")
async def receive_packets(request: Request):
    data_in_bytes: bytes = await request.body()
    data=pickle.loads(data_in_bytes)
    size=data['size']
    packets=data["packets"]
    start_time=time.time()
    # for i in range(packets):
        # await send_packet(size)
    await send_packet_single_connection(size,packets)
    end_time=time.time()
    return "Done with "+str(packets)+" packets of size "+str(size)+" in "+str(end_time-start_time)+" seconds."
