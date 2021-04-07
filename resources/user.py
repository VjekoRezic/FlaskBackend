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
import datetime

from models.user import UserModel
from models.role import RoleModel
from blacklists import BLACKLIST

_profil_parser = reqparse.RequestParser()
_profil_parser.add_argument('email',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_profil_parser.add_argument('ime',
                          type=str,


                            )

_profil_parser.add_argument('prezime',
                          type=str,


                            )

_profil_parser.add_argument('mobitel',
                          type=str,
                            )
                        



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
_user_parser.add_argument('admin_required',
                          type=int,
                            )

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        
        if UserModel.find_by_email(data["email"]):
            return {"message":"Korisnik s tim emailom već postoji"},400
        
        user = UserModel(**data)
        user.save_to_db()
        newuser= UserModel.find_by_email(data["email"])
        access_token= create_access_token(identity=newuser.id, fresh=True, expires_delta=3600)
        refresh_token = create_refresh_token(newuser.id)
        rola= RoleModel.find_by_rolaID(3)


        return {
                "message":"Korisnički račun uspješno stvoren",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user":{"ime":user.ime,
                        "role":rola.rola}
                    
            }, 201

class UserLogin(Resource):
    @cross_origin()
    def post(self):
        trajanje= datetime.timedelta(minutes=60)
        data=_user_parser.parse_args()
        user = UserModel.find_by_email(data["email"])
        if user!=None:
            rola= RoleModel.find_by_rolaID(user.roleID)
        
        if (data["admin_required"]==0) or (data["admin_required"]==None):
            if user and safe_str_cmp(user.lozinka, data["lozinka"]):
                access_token=create_access_token(identity=user.id, fresh=True, expires_delta=trajanje)
                refresh_token=create_refresh_token(identity=user.id)
                return {"message":"Uspješna prijava.",
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user":
                            {"ime":user.ime,
                            "role":rola.rola}
                        },200
            return {"message": "Pogrešan email ili lozinka"}, 401 
        
        if (data["admin_required"]==1):
            if user and safe_str_cmp(user.lozinka, data["lozinka"]) and (user.roleID!=1 and user.roleID!=2):
                return {"message":"Samo administratori imaju pristup!!!"}, 401
            elif user and safe_str_cmp(user.lozinka, data["lozinka"]) and (user.roleID==1 or user.roleID==2):
                access_token=create_access_token(identity=user.id, fresh=True, expires_delta=trajanje)
                refresh_token=create_refresh_token(identity=user.id)
                return {"message":"Uspješna prijava.",
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user":
                            {"ime":user.ime,
                            "role":rola.rola}
                        },200

class UserLogout(Resource):
    @jwt_required
    
    def post(self):
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"message":"Uspješna odjava."},200



class Profil(Resource):

    @jwt_required
    def get(self):
        userID=get_jwt_identity()
        user=UserModel.find_by_id(userID)
        data={
        "email":user.email,
        "ime":user.ime,
        "prezime":user.prezime,
        "mobitel":user.mobitel}

        return {"user":data}

    @jwt_required
    def put(self):
        userID=get_jwt_identity()
        data=_profil_parser.parse_args()
        ime=data["ime"]
        prezime=data["prezime"]
        email=data["email"]
        mobitel=data["mobitel"]
        rezultat=UserModel.update(userID, ime, prezime, email, mobitel)
        return rezultat



        
        

