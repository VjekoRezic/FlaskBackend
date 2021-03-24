from db import db
from models.role import RoleModel

class UserModel(db.Model):
    __tablename__="korisnici"
    
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(256))
    lozinka=db.Column(db.String(256))
    ime=db.Column(db.String(100))
    prezime=db.Column(db.String(100))
    mobitel=db.Column(db.String(100))
    roleID= db.Column(db.Integer, db.ForeignKey("role.id"))
    rola=db.relation(RoleModel , backref="korisnici")

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
    
    def update(userID, ime , prezime, email, mobitel):
        
        user= UserModel.query.filter_by(id=userID).first()
        user.email=email
        user.ime=ime
        user.prezime=prezime
        user.mobitel=mobitel
        db.session.commit()
        return {"message":"Uspješno ste promjenili podatke"}

    def count_users():
        users=db.session.query(UserModel.id).filter(UserModel.roleID==3).count()
        return users

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def is_admin(cls, id):
        user=cls.query.filter_by(id=id).first()
        print (user.roleID)
        if ((user.roleID==1) or (user.roleID==2)):
            return 1
        else:
            return 0

    
    
