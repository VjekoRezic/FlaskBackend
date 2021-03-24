from flask_restful import Resource, reqparse 
from flask import request
from models.items import ItemModel, find_item_by_id, jsons, find_all
from models.brand import BrandModel
from models.kategorija import KategorijaModel
from helpers import admin_required



_item_update_parser=reqparse.RequestParser()
_item_update_parser.add_argument("ime",
                                 type=str )
_item_update_parser.add_argument("cijena", type=float)
_item_update_parser.add_argument("url_slike", type=str)
_item_update_parser.add_argument("brandID", type=int)
_item_update_parser.add_argument("kategorijaID",type=int)
_item_update_parser.add_argument("opis")
_item_update_parser.add_argument("delete", type=int)


_item_post_parser=reqparse.RequestParser()
_item_post_parser.add_argument("ime",type=str, required=True )
_item_post_parser.add_argument("cijena", type=float, required=True)
_item_post_parser.add_argument("url_slike", type=str, required=True)
_item_post_parser.add_argument("brandID", type=int, required=True)
_item_post_parser.add_argument("kategorijaID",type=int, required=True)
_item_post_parser.add_argument("opis", required=True)





class Item(Resource):
    def get(self, id):
        item= find_item_by_id(id)
        
        
        return item
    






class Items(Resource):


    def get(self):
        
        brands=BrandModel.get_all_brands()
        kategorije=KategorijaModel.get_all_categories()

        ###ovdje ide if petlja za filter u try catch vjerojatno 
        try:
            
            brandID=request.args.get("brandID")
            categoryID=request.args.get("kategorijaID")
            

            items=find_all(brandID, categoryID)
            

            if items==[]:
                return {
                    "brendovi":brands,
                    "kategorije":kategorije,
                    "proizvodi":"Nema proizvoda koji odgovaraju vašem filteru."
                }, 200

            

            rezultat={
                "proizvodi":items,
                "brendovi":brands,
                "kategorije":kategorije
                }



            return rezultat, 200

                


        except Exception as e:
            print (str(e))
            return e, 103
    
    @admin_required()
    def post(self):
        data=_item_post_parser.parse_args()
        
        ime=data["ime"],
        cijena=data["cijena"],
        url_slike=data["url_slike"],
        brandID=data["brandID"],
        kategorijaID=data["kategorijaID"],
        opis=data["opis"]
            
        novi_item = ItemModel.post(ime, cijena, url_slike, brandID,kategorijaID,opis)
        return novi_item


class ItemUpdate(Resource):
    @admin_required()
    def get(self, id):
        item= find_item_by_id(id)
        brands=BrandModel.get_all_brands()
        kategorije=KategorijaModel.get_all_categories()
        rezultat={
                "proizvod":item,
                "brendovi":brands,
                "kategorije":kategorije
                }
        
        
        return rezultat

    @admin_required()
    def put(self, id):
        data=_item_update_parser.parse_args()
        ime=data["ime"]
        cijena=data["cijena"]
        url_slike=data["url_slike"]
        brandID=data["brandID"]
        kategorijaID=data["kategorijaID"]
        opis=data["opis"]
        delete=data["delete"]
        
        updated= ItemModel.update(id, ime, cijena, url_slike, brandID, kategorijaID, opis, delete)
        return updated

   


