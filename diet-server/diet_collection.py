import json

# Class implements the logic of the diets collection.
class DietCollection:
    # const strings for a food-item's properties
    STR_NAME = 'name'
    STR_CAL = 'cal'
    STR_SODIUM = 'sodium'
    STR_SUGAR = 'sugar'

    def __init__(self, db):
        self._db = db

    # Inserts a diet item to the db if doesn't already exist.
    def insert_item(self, new_item):
        new_item_name = new_item[self.STR_NAME]
        if self.does_item_name_exist(new_item_name):    # item name already exist.
            return None
        
        result = self._db.insert_one(new_item)
        return new_item_name

    def retrieve_all_items_listed(self):
        cursor = self._db.find({}, {"_id": 0})
        cursor_list = list(cursor)
        return cursor_list
    
    def retrieve_all_items_jsonified(self):
        cursor_list = self.retrieve_all_items_listed()
        cursor_json = json.dumps(cursor_list)
        return cursor_json

    def does_item_name_exist(self, item_name) -> bool:
        found, _ = self.find_item(item_name)
        return found
    
    def find_item(self, key):
        doc = self._db.find_one({self.STR_NAME: key}, {"_id": 0})
        if doc is not None:
            return True, doc
        else:
            return False, None
    
     # returns a new diet item (in a dictionary format) with the given values for its properties.
    @classmethod
    def create_new_diet(cls, name : str, cal : float, sodium : float, sugar : float):
        return {
            cls.STR_NAME: name,
            cls.STR_CAL: cal,
            cls.STR_SODIUM: sodium,
            cls.STR_SUGAR: sugar,
        }
    