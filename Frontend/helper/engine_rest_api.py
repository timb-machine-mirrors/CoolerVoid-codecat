import json
import requests
import warnings
import yaml
warnings.simplefilter("ignore") 


class rest_call:

  def __init__(self, login, password):
    d={}
    with open('helper/api_config.yaml', 'r') as file:
        parsed = yaml.safe_load(file)
    # load external server config at file "config.yaml"
    for key,value in parsed.items():
        if key == "host":
            d['host']=str(value)
    self.host = d['host']
    self.login = login
    self.password = password
    self.token=""
    self.json_output={}
    self.test = False

  def Change_Token(self,token):
    url=self.host+"/api/token"   
    self.token=url
    try:
        r = requests.get(url, verify=False,auth=(token,"x"))
        if r.status_code == 200:
            obj= json.loads(r.content)
            self.token=obj['token']
            self.test = True
        else:
            self.token="0"
            self.test = False
    except:
        self.token="0"
        self.test = False

  def Get_Token(self):
    url=self.host+"/api/token"   
    self.token=url
    try: 
        r = requests.get(url, verify=False,auth=(self.login,self.password))
        if r.status_code == 200:
            obj= json.loads(r.content)
            self.token=obj['token']
            self.test = True
        else:
            self.token="0"
            self.test = False
    except:
        self.token="0"
        self.test = False
         
  def getsinks(self,**input_list):
    url=self.host+"/api/engine/getsinks"
    try:
        r = requests.post(url, verify=False,headers={'Accept' :'application/json, text/plain, */*','Authorization': 'Bearer {}'.format(self.token)},json=input_list) 
        if r.status_code == 200:
            obj= json.loads(r.content)
            self.json_output=obj
        else:
            self.json_output=""
    except:
        self.json_output=""


  def allsinks(self,**input_list):
    url=self.host+"/api/engine/allsinks"
    try:
        r = requests.post(url, verify=False,headers={'Accept' :'application/json, text/plain, */*','Authorization': 'Bearer {}'.format(self.token)},json=input_list) 
        if r.status_code == 200:
            obj= json.loads(r.content)
            self.json_output=obj
        else:
            self.json_output=""
    except:
        self.json_output=""



  def list_sinks(self):
    url=self.host+"/api/engine/list_cache"
    try:
        r = requests.get(url, verify=False,headers={'Accept' :'application/json, text/plain, */*','Authorization': 'Bearer {}'.format(self.token)}) 
        if r.status_code == 200:
            obj= json.loads(r.content)
            self.json_output=obj
        else:
            self.json_output=""
    except:
        self.json_output=""



  def clear_sinks(self):
    url=self.host+"/api/engine/clear"
    try:
        r = requests.get(url, verify=False,headers={'Accept' :'application/json, text/plain, */*','Authorization': 'Bearer {}'.format(self.token)}) 
        if r.status_code == 200:
            obj= json.loads(r.content)
            self.json_output=obj
        else:
            self.json_output=""
    except:
        self.json_output=""
 
