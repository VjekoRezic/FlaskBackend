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
    active=db.Column(db.Integer)

    brandID=db.Column(db.Integer, db.ForeignKey("brendovi.id"))
    brandd=db.relation(BrandModel, backref="brendovi")
    kategorijaID=db.Column(db.Integer, db.ForeignKey("kategorije.id"))
    kategorija=db.relation(KategorijaModel, backref="kategorije")

    def __init__(self,ime, cijena, url_slike, brandID, kategorijaID, opis):
        self.ime=ime
        self.cijena=cijena
        self.url_slike=url_slike
        self.brandID=brandID
        self.kategorijaID=kategorijaID
        self.opis = opis
        self.active=1

    
    def json(self):
        brand = BrandModel.find_brand_by_id(self.brandID)
        kategorija=KategorijaModel.get_category(self.kategorijaID)
        return {
            "id":self.id,
            "ime":self.ime,
            "cijena":self.cijena,
            "url_slike":self.url_slike,
            "brand":brand,
            "kategorija":kategorija,
            "brandID":self.brandID,
            "kategorijaID":self.kategorijaID
            }
    
    def update(id, ime, cijena, url_slike, brandID, kategorijaID, opis, delete):
        item=ItemModel.query.filter_by(id=id).first()
        if ime!=None:
            item.ime=ime
        if cijena!=None:
            item.cijena=cijena
        if url_slike !=None:
            item.url_slike=url_slike
        if brandID !=None:
            item.brandID=brandID
        if kategorijaID !=None:
            item.kategorijaID=kategorijaID
        if opis!=None:
            item.opis=opis
        if delete==1:
            item.active=0
        db.session.commit() 
        return {"message":"Uspješan update proizvoda"}, 200
    
    def post(ime, cijena, url_slike, brandID,kategorijaID,opis):
        novi_item=ItemModel(ime=ime, cijena=cijena, url_slike=url_slike,brandID=brandID, kategorijaID=kategorijaID, opis=opis)
        db.session.add(novi_item)
        db.session.commit()
        return {"message":"Uspješno ste dodali proizvod"}, 200
    
    def count_items():
        items=db.session.query(ItemModel.id).filter(ItemModel.active==1).count()
        return items

    def search(ime):
        ime="%{}%".format(ime)
        
        
        items=db.session.query(ItemModel.id, ItemModel.ime).filter(ItemModel.active==1).filter(ItemModel.ime.ilike(ime)).order_by(ItemModel.ime).all()
        proizvodi=[]
        for x in items:
            obj={
                "id":x[0],
                "ime":x[1]
                }
            proizvodi.append(obj)
        
        itemsObj={"proizvodi":proizvodi}
        
        return itemsObj



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
        "opis":data[6],
        "kategorijaID":data[7],
        "brandID":data[8]
    }
    return json


def find_item_by_id(id):
        data = db.session.query(ItemModel.id, ItemModel.ime, ItemModel.url_slike, ItemModel.cijena, BrandModel.brand, KategorijaModel.kategorija, ItemModel.opis, ItemModel.kategorijaID, ItemModel.brandID).join(
            BrandModel).join(
                KategorijaModel).filter(
                ItemModel.id==id).filter(ItemModel.active==1).first()

        return jsons(data)

def find_all(brandID, categoryID):
    if (brandID != None and categoryID!=None):
        data = db.session.query(ItemModel.id, ItemModel.ime, ItemModel.url_slike, ItemModel.cijena, BrandModel.brand, KategorijaModel.kategorija,ItemModel.opis, ItemModel.kategorijaID, ItemModel.brandID).join(
            BrandModel).join(KategorijaModel).filter(ItemModel.active==1).filter(BrandModel.id==brandID).filter(KategorijaModel.id==categoryID).all()
         
        result=[]
        for x in data:
            result.append(jsons(x))
        return result
    

            
    elif(brandID!=None and categoryID==None):
        data= db.session.query(ItemModel.id, ItemModel.ime, ItemModel.url_slike, ItemModel.cijena, BrandModel.brand, KategorijaModel.kategorija, ItemModel.opis, ItemModel.kategorijaID, ItemModel.brandID).join(
            BrandModel).join(KategorijaModel).filter(ItemModel.active==1).filter(BrandModel.id==brandID).all()
        result=[]
        for x in data:
            result.append(jsons(x))
        return result
                
    elif(brandID==None and categoryID!=None):
        data = db.session.query(ItemModel.id, ItemModel.ime, ItemModel.url_slike, ItemModel.cijena, BrandModel.brand, KategorijaModel.kategorija, ItemModel.opis, ItemModel.kategorijaID, ItemModel.brandID).join(
            BrandModel).join(KategorijaModel).filter(ItemModel.active==1).filter(KategorijaModel.id==categoryID).all()
         
        result=[]
        for x in data:
            result.append(jsons(x))
        return result



    else :
        data = db.session.query(ItemModel.id, ItemModel.ime, ItemModel.url_slike, ItemModel.cijena, BrandModel.brand, KategorijaModel.kategorija, ItemModel.opis, ItemModel.kategorijaID, ItemModel.brandID).join(
        BrandModel).join(
            KategorijaModel).filter(ItemModel.active==1).all()
        result=[]
        for x in data:
            result.append(jsons(x))
        return result


def toSlug(ime):
    slug =ime.replace(' ', '-').lower()
    return slug 

def get_list_of_specific(ids):
    data =  db.session.query(ItemModel.id, ItemModel.ime, ItemModel.url_slike, ItemModel.cijena, BrandModel.brand, KategorijaModel.kategorija, ItemModel.opis, ItemModel.kategorijaID, ItemModel.brandID).join(
        BrandModel).join(
            KategorijaModel).filter(ItemModel.id.in_(ids)).filter(ItemModel.active==1).all()

    result=[]
    for x in data:
            result.append(jsons(x))
    return result


