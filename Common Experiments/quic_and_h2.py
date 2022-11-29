import pickle
import requests
import threading
s = requests.session()

def quic_send():
    configs={}
    configs['packets']=100
    configs['x']=200
    configs['y']=200
    configs_out=pickle.dumps(configs)
    res = s.post('http://127.0.0.1:5002/send', data=configs_out, headers={'Content-Type': 'application/octet-stream'})
    print("Quic:",res.json())
    
def http_send():
    configs={}
    configs['packets']=100
    configs['x']=200
    configs['y']=200
    configs_out=pickle.dumps(configs)
    res = s.post('http://127.0.0.1:5001/send', data=configs_out, headers={'Content-Type': 'application/octet-stream'})
    print("H2:",res.json())

if __name__=='__main__':
    quic = threading.Thread(target=quic_send, args=())
    http = threading.Thread(target=http_send, args=())

    quic.start()
    http.start()

    quic.join()
    http.join()
