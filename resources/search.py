from flask_restful import Resource, reqparse
from models.items import ItemModel

_parser=reqparse.RequestParser()
_parser.add_argument(
    "ime",
    type=str,
    required=True,
    help="Morate unijeti pojam za pretragu ")

class Search(Resource):

    def get(self):
        data = _parser.parse_args()
        ime = data["ime"]
        search=ItemModel.search(ime)
        return search

