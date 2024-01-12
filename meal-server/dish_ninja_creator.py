import requests
from dish_collection import DishCollection

# implements the logic of sending an API request to the Ninja-API
# and creating a dish from the response, parsed to our server requirements.
class DishNinjaCreator:
    def __init__(self):
        self.api_key = ''

    # send an API call to the Ninja-API, requesting for fata asociated with the given dish name.
    # if call is successful - creates a dish item (dictionary) parsed to our server requirements.
    # id no succussful - returns an appropriate response error code
    def try_create_ninja_dish(self, dish_name):
        query = dish_name
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        try:
            response = requests.get(api_url, headers={'X-Api-Key': self.api_key})
        except (requests.ConnectTimeout, requests.ConnectionError): # Handle ninja server isn't reachable
            new_dish = None
            response_error_code = -4
            return new_dish, response_error_code

        response_json = response.json()
        if len(response_json) > 0: # 'name' parameter was not specified in the message body
            new_dish = self._create_dish_from_json(response_json)
            response_error_code = None
        else:
            new_dish = None
            response_error_code = -3
            
        return new_dish, response_error_code
    
    # creates a dish item (dictionary) with the given dish name from data given in JSON format,
    # returns it in a format meets our server requirements, as instructed.
    def _create_dish_from_json(self, response_json):
        notFirst = False
        name = ""
        cal = 0
        size = 0
        sodium = 0
        sugar = 0
        for dish in response_json:
            if notFirst:
                name += f" and {dish['name']}"
            else:
                name = dish["name"]
            notFirst = True
            cal += dish["calories"]
            size += dish["serving_size_g"]
            sodium += dish["sodium_mg"]
            sugar += dish["sugar_g"]
        
        return DishCollection.create_new_dish(name, 0, cal, size, sodium, sugar)