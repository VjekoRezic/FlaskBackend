from flask_restful import Resource, reqparse 
from flask import request
from models.items import ItemModel, find_item_by_id, jsons, find_all
from models.brand import BrandModel
from models.kategorija import KategorijaModel




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
                }, 404

            

            rezultat={
                "proizvodi":items,
                "brendovi":brands,
                "kategorije":kategorije
                }



            return rezultat

                


        except Exception as e:
            print (str(e))
            return e, 103



       