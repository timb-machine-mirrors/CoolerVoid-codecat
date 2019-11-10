# CodeCat - Tool to help in codereview 


CodeCat is a open source tool to help you in codereview, to find sinks and this points follow regex rules...



## How too install, step by step:

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
$ cd backend; python3 wsgi.py &
```

Next step you need save your user to login:
```
$ curl -i -X POST -H "Content-Type: application/json" -d '{"email":"admin2@test.com","username":"admin","password":"rubrik123"}' https://127.0.0.1:5001/api/users -k

```

This end point /api/users, run only one time in first deploy, if you try to send request again to insert user, the endpoint return 404... is for security.


Go to this following "https://127.0.0.1:9093/front/auth/".
Now you can enter in this system auth, use login "admin", pass "rubrik123".


Note: You can load your TLS cert in "wsgi.py".





## Developed by: 

github.com/CoolerVoid
Antonio Costa - coolerlair@gmail.com





