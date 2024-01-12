from enum import Enum
import sys
import json

# Enum listing the key type options for looking up an item in the collection
class KeyType(Enum):
        ID = 1
        NAME = 2

# Class implements the logic of the a general food collection.
class FoodCollection:
    # # const strings for a food-item's properties
    STR_NAME = 'name'
    STR_ID = 'ID'
    STR_CAL = 'cal'
    STR_SODIUM = 'sodium'
    STR_SUGAR = 'sugar'

    def __init__(self, db):
        self._db = db
        self._delete_item_event_handlers = [] # a list of function which will be called-back when an item is deleted
        self._nutritive_properties = (self.STR_CAL, self.STR_SODIUM, self.STR_SUGAR) # A tuple stating the nutritive properties of a food-item.

    # Inserts a food item to the dictionaries and grants it a unique ID, if doesn't already exist.
    def insert_item(self, new_item):
        new_item_name = new_item[self.STR_NAME]
        if self.does_item_name_exist(new_item_name):    # item name already exist.
            return None
        
        docID = {self.STR_ID: 0}
        cur_key = self._db.find_one(docID)["cur_key"] + 1
        result = self._db.update_one(docID, {"$set": {"cur_key": cur_key}})
        new_item[self.STR_ID] = cur_key
        result = self._db.insert_one(new_item)
        sys.stdout.flush()

        return cur_key
    
    # Updates an existing item by its ID
    def update_existing_item(self, new_item, item_id):
        if not self.does_item_id_exist(item_id):    # item doesn't exist - no updating
            return None
        new_item[self.STR_ID] = item_id

        result = self._db.update_one({self.STR_ID: item_id}, {"$set": new_item})
        return item_id
    
    def get_id_by_name(self, item_name):
        _, doc = self.find_item(KeyType.NAME, item_name)
        return doc[self.STR_ID]
    
    def get_name_by_id(self, item_id):
        _, doc = self.find_item(KeyType.ID, item_id)
        return doc[self.STR_NAME]
    
    def retrieve_all_items_listed(self):
        cursor = self._db.find({self.STR_ID: {"$gte": 1}}, {"_id": 0})
        cursor_list = list(cursor)
        return cursor_list
    
    def retrieve_all_items_jsonified(self):
        cursor_list = self.retrieve_all_items_listed()
        cursor_json = json.dumps(cursor_list)
        return cursor_json

    def does_item_id_exist(self, item_id) -> bool:
        found, _ = self.find_item(KeyType.ID, item_id)
        return found

    def does_item_name_exist(self, item_name) -> bool:
        found, _ = self.find_item(KeyType.NAME, item_name)
        return found
    
    # finds and returns the item with the given key, of a given key type (ID or Name) (if exists).
    def find_item(self, key_type : KeyType, key):
        key_to_search_for = self.STR_ID if key_type == KeyType.ID else self.STR_NAME
        doc = self._db.find_one({key_to_search_for: key}, {"_id": 0})
        if doc is not None:
            return True, doc
        else:
            return False, None
        
    # deletes the item with the given key, of a given key type (ID or Name) (if exists). returns its item_id if found.
    def delete_item(self, key_type : KeyType, key):
        found, doc = self.find_item(key_type, key)
        if found:
             item_id = doc[self.STR_ID]
             self._notify_delete_item_event(item_id)
             result = self._db.delete_one({self.STR_ID: item_id})
             if result.acknowledged and result.deleted_count >= 1:  # if result was deleted
                 return True, item_id
             else: # something went wrong
                 return False, None
        else:
             return False, None # Item with given key does not exist in the collection

    # operate all handler functions registered to the 'delete item' event
    def _notify_delete_item_event(self, item_id):
        for handler in self._delete_item_event_handlers:
            handler(item_id)

    # register a new event-handler-function to be notified when an item is going to be deleted.
    def register_delete_item_event_handler(self, handler):
        self._delete_item_event_handlers.append(handler)