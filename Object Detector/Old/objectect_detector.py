import cv2
import time
import os
import json
import base64
import requests
import pickle
import codecs
from threading import Thread
import asyncio
import aiohttp


module = os.environ.get('MODULE_NAME')
print('module is ' + module)
with open("mappings_resize.json", "r") as mappings:
    node_links = json.load(mappings)

s = requests.session()
s.mount("http://", requests.adapters.HTTPAdapter(pool_maxsize=0))


def block_service(bytes_out, next_service, next_module):
    # s = requests.session()
    # global all_sessions
    # global session_index
    # s = all_sessions[session_index%len(all_sessions)]
    # session_index+=1
    global s
    res = s.post('http://' + next_service + ':8001/' + next_module, data=bytes_out, headers={'Content-Type': 'application/octet-stream'})

async def block_service_async(bytes_out, next_service, next_module):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://" + next_service + ":8001/" + next_module,
            data=bytes_out,
            headers={"Content-Type": "application/octet-stream"},
        ) as response:
            return await response.text()

def build_post_data(frame, frame_num, stream, time_dict):
    post_data = {
            'image': frame,
            'kv': {
                'width': 200,
                'height': 200,
                'frameID': frame_num,
                'streamID': stream,
                'time_info': time_dict
            }
        }
    return pickle.dumps(post_data)

async def decode(source, stream):
    print('initialize vieoCapture') # in place of actual logging
    container = cv2.VideoCapture(source)
    container.set(cv2.CAP_PROP_FPS, 30)

    print('starting to read frames') # in place of actual logging
    k = 1
    total_size=0
    while True:
        print(f'reading frame {k}')
        start_time_per_frame = time.time()
        ret, frame = container.read()
        if not ret:
            print('ret is False')
            container.release()
            break
        frame = cv2.resize(frame, (200,200))
        end_time_per_frame = time.time()

        time_dict = {}
        time_dict[module+'_time'] = start_time_per_frame
        time_dict[module+'_end_time'] = end_time_per_frame

        for next_module in node_links[module]['next']:
            next_service = next_module + '-service'
            post_data = build_post_data(frame, k, stream, time_dict)
            thread = Thread(target=block_service, args=(post_data, next_service, next_module,))
            thread.daemon = True
            thread.start()
            #await asyncio.gather(block_service_async(post_data, next_service, next_module))

        k += 1

    return {'source': source, 'processed': k}
