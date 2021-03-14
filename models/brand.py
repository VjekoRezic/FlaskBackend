from db import db

class BrandModel(db.Model):
    __tablename__="brendovi"

    id=db.Column(db.Integer, primary_key=True)
    brand=db.Column(db.String(50))
    opis=db.Column(db.Text)
    url_loga=db.Column(db.String(100))

    def __init__(self, brand, opis, url_loga):
        self.brand=brand
        self.opis=opis
        self.url_loga=url_loga

    def json(self):
        data={
            "brandID":self.id,
            "brand":self.brand,
            "opis":self.opis,
            "url_loga":self.url_loga
        }
        return data

    @classmethod
    def find_brand_by_id(cls, id):
        data= cls.query.filter_by(id=id).scalar()
        return data.brand
    
    @classmethod
    def get_all_brands(cls):
        data=cls.query.all()
        result=[]
        for x in data:
            result.append(x.json())
        return result