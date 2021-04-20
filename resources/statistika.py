from flask_restful import Resource
from models.user import UserModel
from models.kosaricaUser import KosaricaUser
from models.items import ItemModel
from helpers import admin_required


class Stats(Resource):
    @admin_required()
    def get(self):

        narudzbe=KosaricaUser.count_narudzbe()
        users=UserModel.count_users()
        items=ItemModel.count_items()
        return {
            "broj_narudzbi":narudzbe,
            "broj_korisnika":users,
            "broj_proizvoda":items
        }, 200
