from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_cors import cross_origin
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
    jwt_required
)

from models.user import UserModel
from blacklists import BLACKLIST


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('email',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('lozinka',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('ime',
                          type=str,


                            )
_user_parser.add_argument('prezime',
                          type=str,
                            )
_user_parser.add_argument('mobitel',
                          type=str,
                            )

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_email(data["email"]):
            return {"message":"Korisnik s tim emailom već postoji"},400
        
        user = UserModel(**data)
        user.save_to_db()
        newuser= UserModel.find_by_email(data["email"])
        access_token= create_access_token(identity=newuser.id, fresh=True)
        refresh_token = create_refresh_token(newuser.id)


        return {
                "message":"Korisnički račun uspješno stvoren",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user":[
                        {"ime":user.ime}
                    ]
            }, 201

class UserLogin(Resource):
    @cross_origin()
    def post(self):
        data=_user_parser.parse_args()
        user = UserModel.find_by_email(data["email"])

        if user and safe_str_cmp(user.lozinka, data["lozinka"]):
            access_token=create_access_token(identity=user.id, fresh=True)
            refresh_token=create_refresh_token(identity=user.id)
            return {"message":"Uspješna prijava.",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user":[
                        {"ime":user.ime}
                    ] },200
        return {"message": "Pogrešan email ili lozinka"}, 401 

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"message":"Uspješna odjava."},200
