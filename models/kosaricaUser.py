from db import db
from models.user import UserModel 
from datetime import date



class KosaricaUser(db.Model):
    __tablename__="kosarica"

    id=db.Column(db.Integer,primary_key=True)
    korisnikID=db.Column(db.Integer, db.ForeignKey("korisnici.id"))
    korisnik=db.relation(UserModel, backref="kosarica")
    datum=db.Column(db.Date)
    

    def __init__(self, korisnikID, datum):
        self.korisnikID=korisnikID
        self.datum=datum
        


    def save_to_db(korisnikid):
        danas = date.today()
        data = KosaricaUser(korisnikID=korisnikid, datum=danas)
        db.session.add(data)
        db.session.commit()
        iddd=db.session.query(KosaricaUser.id).filter(KosaricaUser.korisnikID==korisnikid).order_by(KosaricaUser.id.desc()).first()
        return iddd[0]
        
