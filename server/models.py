from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class EmailAddress(db.Model):
    __tablename__ = 'emailaddress'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    backup_email = db.Column(db.String)

    @validates('email', 'backup_email')
    def validate_email(self, key, address):
        if not address:
            raise ValueError("Email must be present")
        if not isinstance(address, str):
            raise ValueError("Email must be a string")
        if '@' not in address:
            raise ValueError("Email must have an '@' in the address")
        
        duplicate_email = db.session.query(EmailAddress.id).filter_by(email=address).first()
        if duplicate_email is not None:
            raise ValueError("Email must be unique")
        
        if len(address) > 254:
            raise ValueError("Email is too long.")
        
        if address.split("@")[1] in ["hotmail.com", "yahoo.com"]:
            raise ValueError("Email cannot be a hotmail or yahoo address.")

        return address