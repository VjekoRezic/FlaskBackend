from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
from models.user import UserModel
from functools import wraps

from resources.search import Search
from resources.user import UserRegister , UserLogin, UserLogout, Profil
from resources.items import Item, Items, ItemUpdate
from resources.kosarica import Kosarica , Povijest
from resources.statistika import Stats
from db import db

app= Flask(__name__)

CORS(app, supports_credentials=True)
app.config.from_pyfile("config.cfg")
api= Api(app)

jwt=JWTManager(app)




@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST 

@jwt.user_claims_loader
def add_claims_to_jwt(identity):  
    if UserModel.is_admin(identity) == 1:  
        return {'is_admin': True}
    return {'is_admin': False}
                                                                                                                                                                                                                                                                                                        

api.add_resource(Items, "/proizvodi")
api.add_resource(Item, "/proizvodi/<int:id>")
api.add_resource(UserRegister, "/registracija")
api.add_resource(UserLogin, "/prijava")
api.add_resource(UserLogout, "/odjava")
api.add_resource(Kosarica,"/kosarica")
api.add_resource(Profil, "/profil")
api.add_resource(Povijest, "/povijest")
api.add_resource(ItemUpdate,"/proizvodi/<int:id>/update")
api.add_resource(Stats, "/izvjestaj")
api.add_resource(Search, "/search")



if __name__ == "__main__":
    db.init_app(app)

    app.run(host= "127.0.0.1" , port=5000, debug=True)
