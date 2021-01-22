from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin

from resources.user import UserRegister , UserLogin, UserLogout
from db import db

app= Flask(__name__)

CORS(app, supports_credentials=True)
app.config.from_pyfile("config.cfg")
api= Api(app)

jwt=JWTManager(app)


                                                                                                                                                                                                                                                                                                        












api.add_resource(UserRegister, "/registracija")
api.add_resource(UserLogin, "/prijava")
api.add_resource(UserLogout, "/odjava")



if __name__ == "__main__":
    db.init_app(app)

    app.run(host= "127.0.0.1" , port=5000, debug=True)
