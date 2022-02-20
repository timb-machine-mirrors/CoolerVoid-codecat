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


  def Return_rule_by_ID(self,rule_id):
    url=self.host+"/api/rules/view/"+rule_id
    try:
        r = requests.get(url, verify=False,headers={'Accept' :'application/json, text/plain, */*','Authorization': 'Bearer {}'.format(self.token)}) 
        if r.status_code == 200:
            obj= json.loads(r.content)
            self.json_output=obj
        else:
            self.json_output=""
    except:
        self.json_output=""
         
  def List_rules(self):
    url=self.host+"/api/rules/all"
    try:
        r = requests.get(url, verify=False,headers={'Accept' :'application/json, text/plain, */*','Authorization': 'Bearer {}'.format(self.token)}) 
        if r.status_code == 200:
            obj= json.loads(r.content)
            self.json_output=obj
        else:
            self.json_output=""
    except:
        self.json_output=""
 
  def Insert_rule(self,**input_list):
    url=self.host+"/api/rules/insert"
    print("Send data to:"+url)
    try:
        r = requests.post(url, verify=False,headers={ \
            'Accept' :'application/json, text/plain, */*',\
            'Authorization': 'Bearer {}'.format(self.token)},json=input_list) 
        if r.status_code == 200:
            return "Write data in rules table. <br><img src=\"/static/img/mage1.gif\" height=\"150\" width=\"150\" >"
        else:
            return "Error in Rest API! <br><img src=\"/static/img/mage2.gif\" height=\"150\" width=\"150\" >"
    except:
        return "error in request to insert rule <br><img src=\"/static/img/mage2.gif\" height=\"150\" width=\"150\" >"

        
  def Delete_rule(self,id):
    url=self.host+"/api/rules/delete"
    print(url)
    try:
        r = requests.post(url, verify=False,headers={ \
            'Accept' :'application/json, text/plain, */*',\
            'Authorization': 'Bearer {}'.format(self.token)},json={"id": id}) 
        if r.status_code == 200 or r.status_code == 203:
            return "rule removed ! <br><img src=\"/static/img/mage1.gif\" height=\"150\" width=\"150\" >"
        else:
            return "Error in Rest API. <br><img src=\"/static/img/mage2.gif\" height=\"150\" width=\"150\" >"
    except:
        return "Error in request to delete rule to API. <br><img src=\"/static/img/mage2.gif\" height=\"150\" width=\"150\" >"
        
  def Update_rule(self,**input_list):
    url=self.host+"/api/rules/update"
    print(url)
    try:
        r = requests.post(url, verify=False,headers={ \
            'Accept' :'application/json, text/plain, */*',\
            'Authorization': 'Bearer {}'\
            .format(self.token)},json=input_list) 
        if r.status_code == 200 or r.status_code == 500:
            return "Update rule data resource. <br><img src=\"/static/img/mage1.gif\" height=\"150\" width=\"150\" >"
        else:
            return "Error in Rest API <br><img src=\"/static/img/mage2.gif\" height=\"150\" width=\"150\" >"
    except:
        return "error in request to update rule <br><img src=\"/static/img/mage2.gif\" height=\"150\" width=\"150\" >"
        
