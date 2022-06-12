from flask import abort, request
from application import create_app
import os

app = create_app()
app.config.update(
 SESSION_COOKIE_SECURE=True,
 SESSION_COOKIE_HTTPONLY=True,
 SESSION_COOKIE_SAMESITE='Lax',
)

# low hardening in HTTP headers
@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# allow list of ip address
@app.before_request
def limit_remote_addr():
 with open("application/allow_list/addr.txt",encoding="utf-8") as fp:
  for line in fp:
   if request.remote_addr == line.strip():
    return
 abort(403)  


if __name__ == "__main__":
    app.secret_key = os.environ['CODECAT_APPKEY']
    app.run(host='0.0.0.0',port=50001,debug='False',ssl_context='adhoc')
