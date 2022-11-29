import pickle
import requests

s = requests.session()

if __name__=='__main__':
    configs={}
    configs['packets']=100
    configs['x']=200
    configs['y']=200
    configs_out=pickle.dumps(configs)
    res = s.post('http://127.0.0.1:5002/send', data=configs_out, headers={'Content-Type': 'application/octet-stream'})
    print(res.json())