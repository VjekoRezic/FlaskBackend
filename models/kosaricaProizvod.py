from db import db
from models.kosaricaUser import KosaricaUser
from models.items import ItemModel
from models.brand import BrandModel
from models.kategorija import KategorijaModel


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
        
        db.session.add_all(parsiran_niz)
        db.session.commit()
        


def get_povijest(uid):
    data= db.session.query(KosaricaUser.id ,
     KosaricaUser.datum, 
     KosaricaProizvod.kolicina ,
     ItemModel.id, 
     ItemModel.ime,
     ItemModel.cijena, 
     ItemModel.url_slike, 
     BrandModel.brand,
     KategorijaModel.kategorija ).select_from(
         KosaricaUser).join(
         KosaricaProizvod
     ).join(
         ItemModel
     ).join(
         BrandModel
     ).join(
         KategorijaModel
     ).filter(KosaricaUser.korisnikID==uid).order_by(KosaricaUser.id).all()
    rezultat= parser(data)
    return rezultat



def parser(data):

    parsirano=[]
    obj={"kosaricaID":data[0][0],
        "datum":data[0][1].strftime('%d-%m-%Y'),
        "proizvodi":[]}
    parsirano.append(obj)
    i=0
    for x in data:
        if x[0]== parsirano[i]["kosaricaID"]:
            obj={
                "quantity":x[2],
                "id":x[3],
                "ime":x[4],
                "cijena":x[5],
                "url_slike":x[6],
                "brand":x[7],
                "kategorija":x[8]
            }
            parsirano[i]["proizvodi"].append(obj)

        
        else:
            i=i+1
            obj={"kosaricaID":x[0],
                "datum":x[1].strftime('%d-%m-%Y'),
                "proizvodi":[{
                "quantity":x[2],
                "id":x[3],
                "ime":x[4],
                "cijena":x[5],
                "url_slike":x[6],
                "brand":x[7],
                "kategorija":x[8]
            }
            ]}
            parsirano.append(obj)
    
    return parsirano




