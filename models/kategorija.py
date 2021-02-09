from db import db

class KategorijaModel(db.Model):

    __tablename__="kategorije"

    id=db.Column(db.Integer, primary_key=True)
    kategorija=db.Column(db.String(100))
    
    def json(self):
        data={
            "kategorijaID":self.id,
            "kategorija":self.kategorija
        }
        return data

    @classmethod
    def get_category (cls, id):
        data = cls.query.filter_by(id=id).scalar()
        return data.kategorija
    
    @classmethod
    def get_all_categories(cls):
        data = cls.query.all()
        result=[]
        for x in data:
            result.append(x.json())
        return result