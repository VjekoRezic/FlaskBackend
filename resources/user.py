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
import hashlib
import os 
import datetime
import binascii

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
        data["lozinka"]= (encrypt(data["lozinka"]))
        
        if UserModel.find_by_email(data["email"]):
            return {"message":"Korisnik s tim emailom već postoji"},400
        trajanje= datetime.timedelta(minutes=60)
        user = UserModel(data["email"], data["lozinka"], data["ime"], data["prezime"], data["mobitel"])
        user.save_to_db()
        newuser= UserModel.find_by_email(data["email"])
        access_token= create_access_token(identity=newuser.id, fresh=True, expires_delta=trajanje)
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
            enpass = user.lozinka
            


        
        if (data["admin_required"]==0) or (data["admin_required"]==None):
            if user and ( decrypt(enpass , data["lozinka"])==True):
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
            if user and decrypt(enpass, data["lozinka"])==True and (user.roleID!=1 and user.roleID!=2):
                return {"message":"Samo administratori imaju pristup!!!"}, 401
            elif user and decrypt(enpass, data["lozinka"])==True and (user.roleID==1 or user.roleID==2):
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




def encrypt(lozinka):

    salt = os.urandom(32)

    key = hashlib.pbkdf2_hmac(
        'sha256',
        lozinka.encode('utf-8'),
        salt, 
        100000
    )


    storage =  salt + key
    storage = binascii.b2a_hex(storage)


    return storage

def decrypt(encripted, lozinka):

    encripted= binascii.a2b_hex(encripted)

    salt = encripted[:32]
    enpass= encripted[32:]
    
    #enpass = binascii.a2b_hex(enpass)
    #salt = binascii.a2b_hex(salt)
    
    key = hashlib.pbkdf2_hmac(
        'sha256',
        lozinka.encode('utf-8'),
        salt,
        100000
    )
    
    print (enpass)
    print (key)

    

    if key == enpass:
        return True
    
    else:
        return False
        
        

