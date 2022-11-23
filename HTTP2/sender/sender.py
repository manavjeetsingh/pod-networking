import numpy as np
from fastapi import FastAPI, Request
import os
import pickle
import requests
import time
import http.client
import ssl
import httpx
# Why use FastAPI app?
app = FastAPI()
flow=0
# s = requests.session()
async def send_packet(size):
    data = os.urandom(size)     
    bytes_out = pickle.dumps(data)
    # s = requests.session()
    # res = s.post('http://127.0.0.1:8000/rec', data=bytes_out, headers={'Content-Type': 'application/octet-stream'})

    context = ssl.SSLContext()
    # conn = http.client.HTTPSConnection("127.0.0.1",8000,context=context)
    # conn.request("POST", "/rec",bytes_out,{'Content-Type': 'application/octet-stream'})
    # response = conn.getresponse()
    # print(response.read().decode())

    client = httpx.AsyncClient(http2=True,verify=context)
    r = await client.post('https://127.0.0.1:8000/rec', data=bytes_out,headers={'Content-Type': 'application/octet-stream'})

async def send_packet_single_connection(x,y,packets):

    # calculate a random np array of size x*y
    random_data=np.random.randint(1, 256, size=(3, x, y))
   
    context = ssl.SSLContext()
   
    global flow
    client = httpx.AsyncClient(http2=True,verify=context)
    for i in range(packets):
        timestamp=time.time()
        number=i
        data=pickle.dumps([number,timestamp,random_data,flow])
        r = await client.post('https://130.245.127.102:5000/rec', data=data,headers={'Content-Type': 'application/octet-stream'})
    flow+=1

@app.get("/ping")
def ping():
    return {"status": "Success"}


@app.post("/send")
async def receive_packets(request: Request):
    data_in_bytes: bytes = await request.body()
    data=pickle.loads(data_in_bytes)
    x=data['x']
    y=data['y']
    packets=data["packets"]
    start_time=time.time()
    # for i in range(packets):
    #     await send_packet(size)

    await send_packet_single_connection(x,y,packets)
    end_time=time.time()
    return "Done with "+str(packets)+" packets of size "+str(x)+"*"+str(y)+" in "+str(end_time-start_time)+" seconds."

# if __name__=='__main__':
#     for i in range(100):
#         send_packet(100)