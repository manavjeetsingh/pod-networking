import pickle
import requests
import threading
s = requests.session()



def quic_send1():
    configs={}
    configs['packets']=1000
    configs['x']=200
    configs['y']=200
    configs_out=pickle.dumps(configs)
    res = s.post('http://127.0.0.1:5002/send', data=configs_out, headers={'Content-Type': 'application/octet-stream'})
    print(res.json())

def quic_send2():
    configs={}
    configs['packets']=1000
    configs['x']=200
    configs['y']=200
    configs_out=pickle.dumps(configs)
    res = s.post('http://127.0.0.1:6002/send', data=configs_out, headers={'Content-Type': 'application/octet-stream'})
    print(res.json())

if __name__=='__main__':
    quic1 = threading.Thread(target=quic_send1, args=())
    quic2 = threading.Thread(target=quic_send2, args=())

    quic1.start()
    quic2.start()

    quic1.join()
    quic2.join()
