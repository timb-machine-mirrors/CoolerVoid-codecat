import json
import requests
import warnings
import yaml
warnings.simplefilter("ignore") 


class rest_call:

  def __init__(self, login, password):
    d={}
    document = open("helper/api_config.yaml", 'r')
    parsed = yaml.load(document, Loader=yaml.FullLoader)
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


  def Return_User_by_ID(self,user_id):
    url=self.host+"/api/users/view/"+user_id
    try:
        r = requests.get(url, verify=False,headers={'Accept' :'application/json, text/plain, */*','Authorization': 'Bearer {}'.format(self.token)}) 
        if r.status_code == 200:
            obj= json.loads(r.content)
            self.json_output=obj
        else:
            self.json_output=""
    except:
        self.json_output=""
         
  def List_Users(self):
    url=self.host+"/api/users/all"
    try:
        r = requests.get(url, verify=False,headers={'Accept' :'application/json, text/plain, */*','Authorization': 'Bearer {}'.format(self.token)}) 
        if r.status_code == 200:
            obj= json.loads(r.content)
            self.json_output=obj
        else:
            self.json_output=""
    except:
        self.json_output=""
 
  def Insert_User(self,email,username,password,owner):
    url=self.host+"/api/users/insert"
    print(url)
    try:
        r = requests.post(url, verify=False,headers={ \
            'Accept' :'application/json, text/plain, */*',\
            'Authorization': 'Bearer {}'.format(self.token)},json={"email": email,"username": username,"password": password,"owner": owner}) 
        if r.status_code == 200:
            return "Write data in users table. <br><img src=\"/static/img/mage1.gif\" height=\"150\" width=\"150\" >"
        else:
            return "Error in Rest API! <br><img src=\"/static/img/mage2.gif\" height=\"150\" width=\"150\" >"
    except:
        return "error in request to insert user <br><img src=\"/static/img/mage2.gif\" height=\"150\" width=\"150\" >"

        
  def Delete_User(self,id):
    url=self.host+"/api/users/delete"
    print(url)
    try:
        r = requests.post(url, verify=False,headers={ \
            'Accept' :'application/json, text/plain, */*',\
            'Authorization': 'Bearer {}'.format(self.token)},json={"id": id}) 
        if r.status_code == 200 or r.status_code == 203:
            return "User account removed ! <br><img src=\"/static/img/mage1.gif\" height=\"150\" width=\"150\" >"
        else:
            return "Error in Rest API. <br><img src=\"/static/img/mage2.gif\" height=\"150\" width=\"150\" >"
    except:
        return "Error in request to delete user to API. <br><img src=\"/static/img/mage2.gif\" height=\"150\" width=\"150\" >"
        
  def Update_User(self,id,email,username,password,owner):
    url=self.host+"/api/users/update"
    print(url)
    try:
        r = requests.post(url, verify=False,headers={ \
            'Accept' :'application/json, text/plain, */*',\
            'Authorization': 'Bearer {}'\
            .format(self.token)},json={"id": id,"email": email,"username": username,"password": password,"owner": owner}) 
        if r.status_code == 200 or r.status_code == 500:
            return "Update user data resource.<br> <img src=\"/static/img/mage1.gif\" height=\"150\" width=\"150\" >"
        else:
            return "Error in Rest API <br> <img src=\"/static/img/mage2.gif\" height=\"150\" width=\"150\" >"
    except:
        return "error in request to update user <br> <img src=\"/static/img/mage2.gif\" height=\"150\" width=\"150\" >"


  def Token_to_id(self,token):
    url=self.host+"/api/users/token2id"
    print(url)
    try:
        r = requests.post(url, verify=False,headers={ \
            'Accept' :'application/json, text/plain, */*',\
            'Authorization': 'Bearer {}'.format(self.token)},json={"token": token}) 
        if r.status_code == 200 or r.status_code == 203:
            return r.text
        else:
            return "Error in Rest API."
    except:
        return "Error in request to delete user to API."
        
