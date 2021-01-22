from db import db

class UserModel(db.Model):
    __tablename__="korisnici"
    
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(256))
    lozinka=db.Column(db.String(256))
    ime=db.Column(db.String(100))
    prezime=db.Column(db.String(100))
    mobitel=db.Column(db.String(100))
    roleID= db.Column(db.Integer)

    def __init__(self, email, lozinka, ime, prezime, mobitel):
        self.email = email
        self.lozinka = lozinka
        self.ime = ime
        self.prezime = prezime
        self.mobitel = mobitel
        self.roleID = 3

    
    def json(self):
        return {"id":self.id,
                "email":self.email
                }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
