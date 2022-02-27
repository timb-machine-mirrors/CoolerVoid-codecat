from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['UPLOAD_PATH'] = '../sandbox_of_sources'
db = SQLAlchemy()
db.init_app(app)

def create_app():
 with app.app_context():
  # Imports
  from . import routes
  db.create_all()
 return app


if __name__ == '__main__':
    if not os.path.exists('db/data.db'):
        db.create_all()
    app.run(debug=True)
