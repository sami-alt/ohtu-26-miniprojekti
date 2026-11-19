from os import getenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from dotenv import load_dotenv


load_dotenv()

test_env = getenv("TEST_ENV") == "true"
print(f"Test environment: {test_env}")

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

with app.app_context():
    @event.listens_for(db.engine, "connect")
    def set_pragma(connection, connection_record):
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.close()