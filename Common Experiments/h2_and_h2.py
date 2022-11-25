import pickle
import requests
import threading
s = requests.session()



def http_send1():
    configs={}
    configs['packets']=1000
    configs['x']=100
    configs['y']=100
    configs_out=pickle.dumps(configs)
    res = s.post('http://127.0.0.1:5001/send', data=configs_out, headers={'Content-Type': 'application/octet-stream'})
    print(res.json())

def http_send2():
    configs={}
    configs['packets']=1000
    configs['x']=100
    configs['y']=100
    configs_out=pickle.dumps(configs)
    res = s.post('http://127.0.0.1:6001/send', data=configs_out, headers={'Content-Type': 'application/octet-stream'})
    print(res.json())

if __name__=='__main__':
    http1 = threading.Thread(target=http_send1, args=())
    http2 = threading.Thread(target=http_send2, args=())

    http1.start()
    http2.start()

    http1.join()
    http2.join()
