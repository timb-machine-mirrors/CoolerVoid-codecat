# CodeCat - Tool to help in static code analysis
CodeCat is an open-source tool to help you find/track user input sinks and bugs using static code analysis. These points follow regex rules.
<img align="center" src="https://github.com/CoolerVoid/codecat/blob/master/doc/images/Screenshot.png">
<br>

Current rules for C,C++,GO,Python,javascript,Swift,PHP,Ruby,ASP,Kotlin,Dart and Java.(you can create your rules)

## video
https://www.youtube.com/watch?v=Bmfhsr3BvyA

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

Run backend and frontend:
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

These endpoint /API/users run only once in the first deployment. If you try to send a request again to insert a user, the endpoint return 404 is security to block resources of possible attacks.

Go to the following "https://127.0.0.1:50093/front/auth/".
Now you can enter this system-auth, use login "admin", pass "rubrik123".

*Note About TLS:* You can configure and load your TLS cert in "wsgi.py".


# Production

 Suppose you need to run in production. So I recommend another way.
```
$ gunicorn -b 127.0.0.1:50001 wsgi:app
```

If you want, you can use TLS with CERT resources:
```
$ gunicorn --certfile=server.crt --keyfile=server.key -b 127.0.0.1:50001 wsgi:app
```
The same command to frontend, but you need to use port 50093.

Remember, codecat have a function to recursive reading in the directory. This function with user input is a dangerous issue called **"path traversal"**. Use this tool in a controlled place. My machine is a local virtual machine to run a codecat. Looking at the firewall context, you can block different IP addresses to limit access of codecat for example.


## How can you use it?
Please study the doc.
https://github.com/CoolerVoid/codecat/blob/master/doc/raptor.pdf

So any questions, create an issue, and I can try to help you.


## Note
The purpose of this tool is to use in code review, take attention if you have a proper authorization before to use that. I do not have responsibility for your actions. You can use a hammer to construct a house or destroy it, choose the law path, don't be a bad guy, remember.


## Developed by: 

github.com/CoolerVoid
Antonio Costa - coolerlair@gmail.com





