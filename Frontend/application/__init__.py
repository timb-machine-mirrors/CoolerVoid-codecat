from flask import Flask

app = Flask(__name__)

def create_app():
 with app.app_context():
  # Imports
  from . import routes
 return app

if __name__ == '__main__':
    app.run()
