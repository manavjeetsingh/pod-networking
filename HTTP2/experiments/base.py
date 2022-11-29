import pickle
import requests

s = requests.session()

if __name__=='__main__':
    configs={}
    configs['packets']=100
    configs['x']=150
    configs['y']=150
    configs_out=pickle.dumps(configs)
    res = s.post('http://127.0.0.1:5001/send', data=configs_out, headers={'Content-Type': 'application/octet-stream'})
    print(res.json())