import pickle
import requests

s = requests.session()

if __name__=='__main__':
    configs={}
    configs['packets']=1000
    configs['size']=71000
    configs_out=pickle.dumps(configs)
    res = s.post('http://127.0.0.1:8001/send', data=configs_out, headers={'Content-Type': 'application/octet-stream'})
    print(res.json())