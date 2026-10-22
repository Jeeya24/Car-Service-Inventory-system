import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Add parent directory to path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

def alter_password_hash_length():
    """
    Alter the password_hash column length in the user and employee tables
    """
    with app.app_context():
        db.session.execute(text('ALTER TABLE user MODIFY password_hash VARCHAR(255);'))
        db.session.execute(text('ALTER TABLE employee MODIFY password_hash VARCHAR(255);'))
        db.session.commit()
        print("Successfully altered password_hash column length to 255 characters")

if __name__ == "__main__":
    alter_password_hash_length()
