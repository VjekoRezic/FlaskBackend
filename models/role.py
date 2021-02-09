from db import db

class RoleModel(db.Model):
    __tablename__="role"

    id=db.Column(db.Integer, primary_key=True)
    rola=db.Column(db.String(100))


    def __init__(self, rola):
        self.rola=rola

    def json(self):
        return self.rola
    
    @classmethod
    def find_by_rolaID(cls, id):
        return cls.query.filter_by(id=id).first()