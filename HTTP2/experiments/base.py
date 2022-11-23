import pickle
import requests

s = requests.session()

if __name__=='__main__':
    configs={}
    configs['packets']=1000
    configs['x']=1920
    configs['y']=1080
    configs_out=pickle.dumps(configs)
    res = s.post('http://130.245.127.102:5001/send', data=configs_out, headers={'Content-Type': 'application/octet-stream'})
    print(res.json())