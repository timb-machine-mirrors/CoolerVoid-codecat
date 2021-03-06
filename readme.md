# CodeCat - Tool to help in static code analysis

CodeCat is a open source tool to help you in static code analysis, to find/track sinks and bugs, this points follow regex rules... 
<img align="center" src="https://github.com/CoolerVoid/codecat/blob/master/doc/images/Screenshot.png">
<br>

Current rules for C,C++,GO,Python,javascript,Swift,PHP,Ruby,ASP and Java.(you can create your rules)

## How too install, step by step:
<img align="right" width="240" height="220" src="https://github.com/CoolerVoid/codecat/blob/master/doc/images/codecat01.png">

Go to CodeCat directory, install backend and frontend libs:
```
$ cd Front
$ sudo python3 -m pip install -r requirements.txt
$ cd ..
$ cd Backend
$ sudo python3 -m pip install -r requirements.txt
```

Run backend and frontend...
```
$ cd Codecat
$ cd Frontend; python3 wsgi.py &
$ cd ..
$ cd Backend; python3 wsgi.py &
```

Next step you need save your user to login:
```
$ curl -i -X POST -H "Content-Type: application/json" -d '{"email":"admin2@test.com","username":"admin","password":"rubrik123"}' https://127.0.0.1:50001/api/users -k

```

These endpoint /API/users run only once in the first deployment. If you try to send a request again to insert a user, the endpoint return 404... is for security.


Go to the following "https://127.0.0.1:50093/front/auth/".
Now you can enter this system-auth, use login "admin", pass "rubrik123".

*Note About TLS:* You can configure and load your TLS cert in "wsgi.py".


## How can you use it?
Please study the doc.
https://github.com/CoolerVoid/codecat/blob/master/doc/raptor.pdf








## Developed by: 

github.com/CoolerVoid
Antonio Costa - coolerlair@gmail.com





