from db import db
from models.brand import BrandModel
from models.kategorija import KategorijaModel

class ItemModel(db.Model):
    __tablename__="proizvodi"

    id=db.Column(db.Integer, primary_key=True)
    ime=db.Column(db.String(50))
    cijena=db.Column(db.Float(precision=2))
    url_slike=db.Column(db.String(100))
    opis=db.Column(db.Text)

    brandID=db.Column(db.Integer, db.ForeignKey("brendovi.id"))
    brandd=db.relation(BrandModel, backref="brendovi")
    kategorijaID=db.Column(db.Integer, db.ForeignKey("kategorije.id"))
    kategorija=db.relation(KategorijaModel, backref="kategorije")

    def __init__(self):
        self.ime=ime
        self.cijena=cijena
        self.url_slike=url_slike
        self.brandID=brandID
        self.kategorijaID=kategorijaID
        self.opis = opis

    
    def json(self):
        brand = BrandModel.find_brand_by_id(self.brandID)
        kategorija=KategorijaModel.get_category(self.kategorijaID)
        return {
            "id":self.id,
            "ime":self.ime,
            "cijena":self.cijena,
            "url_slike":self.url_slike,
            "brand":brand,
            "kategorija":kategorija
            }

   # @staticmethod
   # def find_item_by_id(id):
    #    data = db.session.query(ItemModel).join(
    #        BrandModel).join(
     #           KategorijaModel).filter(
    #            ItemModel.id==id).first()

    #    return data


    #@staticmethod
    #def find_all():
    #    data = db.session.query(ItemModel).join(
    #        BrandModel).join(
    #            KategorijaModel).all()
    #    return data

def jsons(data):
    slug= toSlug(data[1])
    json={
        "id": data[0],
        "ime":data[1],
        "url_slike":data[2],
        "cijena":'{0:.2f}'.format(float(data[3])),
        #"cijena":data[3],
        "brand":data[4],
        "kategorija":data[5],
        "slug":slug,
        "opis":data[6]
    }
    return json


def find_item_by_id(id):
        data = db.session.query(ItemModel.id, ItemModel.ime, ItemModel.url_slike, ItemModel.cijena, BrandModel.brand, KategorijaModel.kategorija, ItemModel.opis).join(
            BrandModel).join(
                KategorijaModel).filter(
                ItemModel.id==id).first()

        return jsons(data)

def find_all(brandID, categoryID):
    if (brandID != None and categoryID!=None):
        data = db.session.query(ItemModel.id, ItemModel.ime, ItemModel.url_slike, ItemModel.cijena, BrandModel.brand, KategorijaModel.kategorija,ItemModel.opis).join(
            BrandModel).join(KategorijaModel).filter(BrandModel.id==brandID).filter(KategorijaModel.id==categoryID).all()
         
        result=[]
        for x in data:
            result.append(jsons(x))
        return result
    

            
    elif(brandID!=None and categoryID==None):
        data= db.session.query(ItemModel.id, ItemModel.ime, ItemModel.url_slike, ItemModel.cijena, BrandModel.brand, KategorijaModel.kategorija, ItemModel.opis).join(
            BrandModel).join(KategorijaModel).filter(BrandModel.id==brandID).all()
        result=[]
        for x in data:
            result.append(jsons(x))
        return result
                
    elif(brandID==None and categoryID!=None):
        data = db.session.query(ItemModel.id, ItemModel.ime, ItemModel.url_slike, ItemModel.cijena, BrandModel.brand, KategorijaModel.kategorija, ItemModel.opis).join(
            BrandModel).join(KategorijaModel).filter(KategorijaModel.id==categoryID).all()
         
        result=[]
        for x in data:
            result.append(jsons(x))
        return result



    else :
        data = db.session.query(ItemModel.id, ItemModel.ime, ItemModel.url_slike, ItemModel.cijena, BrandModel.brand, KategorijaModel.kategorija, ItemModel.opis).join(
        BrandModel).join(
            KategorijaModel).all()
        result=[]
        for x in data:
            result.append(jsons(x))
        return result


def toSlug(ime):
    slug =ime.replace(' ', '-').lower()
    return slug 

def get_list_of_specific(ids):
    data =  db.session.query(ItemModel.id, ItemModel.ime, ItemModel.url_slike, ItemModel.cijena, BrandModel.brand, KategorijaModel.kategorija, ItemModel.opis).join(
        BrandModel).join(
            KategorijaModel).filter(ItemModel.id.in_(ids)).all()

    result=[]
    for x in data:
            result.append(jsons(x))
    return result
