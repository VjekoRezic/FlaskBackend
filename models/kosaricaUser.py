from db import db
from models.user import UserModel 



class KosaricaUser(db.Model):
    __tablename__="kosarica"

    id=db.Column(db.Integer,primary_key=True)
    korisnikID=db.Column(db.Integer, db.ForeignKey("korisnici.id"))
    korisnik=db.relation(UserModel, backref="kosarica")
    

    def __init__(self, korisnikID):
        self.korisnikID=korisnikID
        


    def save_to_db(korisnikid):
        data = KosaricaUser(korisnikID=korisnikid)
        db.session.add(data)
        db.session.commit()
        iddd=db.session.query(KosaricaUser.id).filter(KosaricaUser.korisnikID==korisnikid).order_by(KosaricaUser.id.desc()).first()
        return iddd[0]
        
