import pymongo
from dish_collection import DishCollection
from meal_collection import MealCollection

# initialize the dishes and meals collection and the global logic objects of the server application
def init():
    global dish_collection
    global meal_collection

    client = pymongo.MongoClient("mongodb://mongo:27017/")
    db = client["mongodb"]
    dish_col_db = db["dishes"]
    meal_col_db = db["meals"]

    if dish_col_db.find_one({"ID": 0}) is None:  # first time starting up this service as no document with ID == 0 exists
    # insert a document into the database to have one "ID" index that starts at 0 and a field named "cur_key"
        dish_col_db.insert_one({"ID": 0, "cur_key": 0})

    if meal_col_db.find_one({"ID": 0}) is None:
        meal_col_db.insert_one({"ID": 0, "cur_key": 0})

    dish_collection = DishCollection(dish_col_db)
    meal_collection = MealCollection(meal_col_db, dish_collection)
