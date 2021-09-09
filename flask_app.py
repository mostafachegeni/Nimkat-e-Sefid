from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


application = Flask(__name__)
application.config.from_object(Config)
db = SQLAlchemy(application)
migrate = Migrate(application, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


#from flask import Flask
#application = Flask(__name__)

@application.route("/")
def hello():
	return "hello!************"
#	return "<h1 style='color:blue'>Hello There!</h1>"

#if __name__ == "__main__":
#	application.run(host='0.0.0.0')
