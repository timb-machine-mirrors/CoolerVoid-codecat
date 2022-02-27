from flask import Flask

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * (1024 * 1024)    # max size of upload file is 50 mb
app.config['UPLOAD_EXTENSIONS'] = ['.zip']
app.config['UPLOAD_PATH'] = '../sandbox_of_sources'

def create_app():
 with app.app_context():
  # Imports
  from . import routes
 return app

if __name__ == '__main__':
    app.run()
