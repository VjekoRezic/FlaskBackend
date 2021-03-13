from db import db
from models.kosaricaUser import KosaricaUser
from models.items import ItemModel


class KosaricaProizvod(db.Model):
    __tablename__="proizvodi_kosarica"
    id=db.Column(db.Integer, primary_key=True)
    kosaricaID=db.Column(db.Integer, db.ForeignKey("kosarica.id"))
    proizvodID=db.Column(db.Integer, db.ForeignKey("proizvodi.id"))
    kolicina=db.Column(db.Integer)
    kosarica=db.relation(KosaricaUser, backref="proizvodi_kosarica")
    proizvod=db.relation(ItemModel, backref="proizvodi_kosarica")


    def __init__(self, kosaricaID, proizvodID, kolicina):
        self.kosaricaID=kosaricaID
        self.proizvodID=proizvodID
        self.kolicina=kolicina
    

    def spremi_proizvode(parsiran_niz):
        print("uslo")
        db.session.add_all(parsiran_niz)
        db.session.commit()
        print("radi")
