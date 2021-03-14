from flask_restful import Resource, reqparse 
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.kosaricaUser import KosaricaUser
from models.kosaricaProizvod import KosaricaProizvod
from models.items import get_list_of_specific
import json



class Kosarica(Resource):
    @jwt_required
    def post(self):

        
        userID=get_jwt_identity()
        proi=[]
        a=KosaricaUser.save_to_db(userID)
        
        
        try:
            parsejson = request.get_json()
            proizvodi = parsejson['proizvodi']
           
            for x in proizvodi:
                kp= KosaricaProizvod(kosaricaID=a, proizvodID=x["id"], kolicina=x["quantity"])
                proi.append(kp)
            KosaricaProizvod.spremi_proizvode(proi)
            return {"message":"Uspješna kupovina."
                }, 200
        
        except Exception as e:
            return(str(e))
        
        #print(data["proizvodi"][1])
       # a=KosaricaUser.save_to_db(userID)
       
    
    #@jwt_required
    def get(self):
        try:
            ids=request.args.getlist('id', type=int)
            rezultat= get_list_of_specific(ids)
            return {"proizvodi":rezultat}

            
        except Exception as e:
            return(str(e))



        

