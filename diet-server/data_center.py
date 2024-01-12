import pymongo
from diet_collection import DietCollection

# initialize the diets collection and the global logic object of the server application
def init():
    global diet_collection

    client = pymongo.MongoClient("mongodb://mongo:27017/")
    db = client["mongodb"] # 'mongodb' is the name of the db
    diet_col_db = db["diets"]

    diet_collection = DietCollection(diet_col_db)
    
