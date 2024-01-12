# FeedMe Server - API Documentation
This API designed by Dr. Danny Yellin, supplies CRUD opperations of a restaurant's entities: `dish`, `meal`, `diet`.

## Models
### A dish
Given by its name, which may consist many products.  
On a record creation, the program fetches the dish's information from [api-ninjas](api-ninjas.com/api/nutrition) by the given name, and computes its nutritional values by summing the the nutritional values of the individual products that make up this dish:
- The number of calories
- The serving size (in grams)
- The amount of sodium (in mg)
- The amount of sugar (in grams)  

Each dish resource is expressed by the following JSON object:
```
{
    "name": <string>,
    "ID": <number>,         # positive integer
    "cal": <number>,
    "size": <number>,
    "sodium": <number>,
    "sugar": <number>
}
```  
Example:
```
{
    "name": "focaccia",
    "ID": 2,
    "cal": 251.9,
    "size": 100.0,
    "sodium": 570,
    "sugar": 1.8
}
```

### A meal
Specifes the 3 dish IDs that comprise that meal (appetizer, main, desert).  
On a record creation, the program computes the total nutritional values of that meal by summing those values of the individual dishes that make up the meal.  

Each meal resource is expressed by the following JSON object:
```
{
    "name": <string>,       # name of meal
    "ID": <number>,         # ID of meal
    "appetizer": <number>,  # ID of appetizer dish
    "main": <number>,       # ID of main dish
    "dessert": <number>,    # ID of dessert dish
    "cal": <number>,        # total number of calories in meal
    "sodium": <number>,     # total amount of sodium in meal
    "sugar": <number>       # total amount of sugar in meal
}
```  
Example:
```
{
    "name": "chicken special",
    "ID": 2,
    "appetizer": 3,
    "main": 16,
    "dessert": 15,
    "cal": 812.4,
    "sodium": 1018,
    "sugar": 1.9000000000000001
}
```

- If one of the dishes of the meal changes - the nutritional values of the meal are updated accordingly.
- If one of the dishes are deleted - the appropriate property and all of the nutritional values turn to `JSON-null`
    
    ➡ Example - say that the `dish` with `ID: 3` which had been set to be the meal's `appetizer` was deleted:
    ```
    {
        "name": "chicken special",
        "ID": 2,
        "appetizer": null,
        "main": 16,
        "dessert": 15,
        "cal": null,
        "sodium": null,
        "sugar": null
    }
    ```

### A diet
Each diet resource is expressed by the following JSON object:
```
{
    "name": <string>,
    "cal": <number>,
    "sodium": <number>,
    "sugar": <number>
}
```
Example:
```
{
    "name": "low sodium",
    "cal": 5000,
    "sodium": 5,
    "sugar": 50
}
```

## Resources
### /dishes
A collection of all the dishes  
`POST` - will add a `dish` of the given `name`
- Ports: `5001`
- Data Params of type `application/json`
    ```
    {
        "name": <string>
    }
    ```
- Success Response:
    - Code: `201`
    - Content: `<number>` - a positive integer, the created dish ID.
- Error Response:
    - Request content-type is not `application/json`
      - Code: `415 Unsupported Media Type`
      - Content: `0`
    - The 'name'parameter was not specified in the message body
        - Code: `422 Unprocessable Content`
        - Content: `-1`
    - Dish of given name already exists
        - Code: `422 Unprocessable Content`
        - Content: `-2`
    - [api-ninjas](api-ninjas.com/api/nutrition) does not recognize this dish name
        - Code: `422 Unprocessable Content`
        - Content: `-3`
    - [api-ninjas](api-ninjas.com/api/nutrition) was no reachable
        - Code: `504 Gateway Timeout`
        - Content: `-4`

`GET` - will return the a JSON array listing all `dish`es, in ascending order by their `ID`.
- Ports: `80`, `5001`
- Response:
    - Code: `200`
    - Content: `[ <dish JSON>, <dish JSON>, <dish JSON>, ...]`  
    If no records created, the array is empty: `[]`

---
### /dishes/:id
`GET` - will return the the JSON representation of the `dish` with the given `id`.  
- Ports: `80`, `5001`
- URL Params (required):
    - `id: <number>` - positive integer
- Success Response:
    - Code: `200`
    - Content: `<dish JSON>`
- Error Response:
    - The dish `ID` was not found:
        - Code: `404 Not Found`
        - Content: `-5`

`DELETE` - removes the `dish` with the given `id` from the `/dishes` resource.
- URL Params (required):
    - `id=<number>` - positive integer
- Success Response:
    - Code: `200`
    - Content: `<number>` - a positive integer, the removed dish ID.
- Error Response:
    - The dish `ID` was not found:
        - Code: `404 Not Found`
        - Content: `-5`

---
### /dishes/:name
`GET` - will return the the JSON representation of the `dish` with the given `name`.  
- Ports: `80`, `5001`
- URL Params:
    - `name: <string>` (required)
- Success Response:
    - Code: `200`
    - Content: `<dish JSON>`
- Error Response:
    - The dish `name` was not found:
        - Code: `404 Not Found`
        - Content: `-5`

`DELETE` - removes the dish with the given `name` from the `/dishes` resource.
- Ports: `5001`
- URL Params:
    - `name: <string>` (required)
- Success Response:
    - Code: `200`
    - Content: `<number>` - a positive integer, the removed dish `ID` (Notice: NOT `name`).
- Error Response:
    - The dish `name` was not found:
        - Code: `404 Not Found`
        - Content: `-5`
---
---
### /meals
A collection of all the meals  
`POST` - will add a `meal` of the given `name` with the given 3 dishes `ID`s:
- Ports: `5001`
- Data Params of type `application/json`
    ```
    {
        "name": <string>,
        "appetizer": <number>,
        "main": <number>,
        "dessert": <number>
    }
    ```
    Example:
    ```
    {
        "name": "chicken special",
        "appetizer": 2,
        "main": 3,
        "dessert": 6
    }
    ```
- Success Response:
    - Code: `201`
    - Content: `<number>` - a positive integer, the created meal ID.
- Error Response:
    - Request content-type is not `application/json`
      - Code: `415 Unsupported Media Type`
      - Content: `0`
    - One of the required properties in the body was not given or not specified correctly
        - Code: `422 Unprocessable Content`
        - Content: `-1`
    - Meal of given name already exists
        - Code: `422 Unprocessable Content`
        - Content: `-2`
    - One of the sent dish IDs (appetizer, main, dessert) does not exist.
        - Code: `422 Unprocessable Content`
        - Content: `-6`

`GET` - will return a JSON array listing all `meal`s OR meals satisfying a `diet`, if its name is supplied in `query string`, in ascending order by their `ID`.  
- Ports: `80`, `5001`
- Query string (optional):
    - `diet=<string>` - value is a diet name
    Example: `/meals?diet=low sodium`
- Success Response:
    - Code: `200`
    - Content: `[ <meal JSON>, <meal JSON>, <meal JSON>, ...]`  
    If no records created, the array is empty: `[]`
- Error Response:
    - The diet `name` was not found:
        - Code: `404 Not Found`
        - Content: `-5`
---
### /meals/:id
`GET` - will return the the JSON representation of the `meal` with the given `id`.  
- Ports: `80`, `5001`
- URL Params (required):
    - `id: <number>` - positive integer
- Success Response:
    - Code: `200`
    - Content: `<meal JSON>`
- Error Response:
    - The meal `id` was not found:
        - Code: `404 Not Found`
        - Content: `-5`

`DELETE` - removes the `meal` with the given `id` from the `/meals` resource.
- Ports: `5001`
- URL Params (required):
    - `id=<number>` - positive integer
- Success Response:
    - Code: `200`
    - Content: `<number>` - a positive integer, the removed meal ID.
- Error Response:
    - The meal `id` was not found:
        - Code: `404 Not Found`
        - Content: `-5`

`PUT` - will update the `meal` with the given `id` to the new properties supplied in the `body`.
- Ports: `5001`
- Data Params of type `application/json`
    ```
    {
        "name": <string>,       # original name OR non-existing name
        "appetizer": <number>,
        "main": <number>,
        "dessert": <number>
    }
    ```
- Success Response:
    - Code: `200`
    - Content: `<number>` - a positive integer, the updated meal ID.
- Error Response:
    - Request content-type is not `application/json`
      - Code: `415 Unsupported Media Type`
      - Content: `0`
    - One of the required properties in the `body` was not given or not specified correctly
        - Code: `422 Unprocessable Content`
        - Content: `-1`
    - Meal of given name already exists (and isn't the original meal name)
        - Code: `422 Unprocessable Content`
        - Content: `-2`
    - One of the sent dish IDs (appetizer, main, dessert) does not exist.
        - Code: `422 Unprocessable Content`
        - Content: `-6`

---
### /meals/:name
`GET` - will return the the JSON representation of the `meal` with the given `name`.  
- Ports: `80`, `5001`
- URL Params:
    - `name: <string>` (required)
- Success Response:
    - Code: `200`
    - Content: `<meal JSON>`
- Error Response:
    - The meal `name` was not found:
        - Code: `404 Not Found`
        - Content: `-5`

`DELETE` - removes the `meal` with the given `name` from the `/dishes` resource.
- Ports: `5001`
- URL Params:
    - `name: <string>` (required)
- Success Response:
    - Code: `200`
    - Content: `<number>` - a positive integer, the removed meal `ID` (Notice: NOT `name`).
- Error Response:
    - The meal `name` was not found:
        - Code: `404 Not Found`
        - Content: `-5`
---
---
### /diets
A collection of all the diets  
`POST` - will add a `diet` of the given `name` with the given 3 nutritional values:
- Ports: `5002`
- Data Params of type `application/json`
    ```
    {
        "name": <string>,
        "cal": <number>,
        "sodium": <number>,
        "sugar": <number>
    }
    ```
    Example:
    ```
    {
        "name": "low sodium",
        "cal": 5000,
        "sodium": 5,
        "sugar": 50
    }
    ```
- Success Response:
    - Code: `201`
    - Content: `Diet <name> was created successfully`
- Error Response:
    - Diet of given name already exists
        - Code: `422 Unprocessable Entity`
        - Content: `Diet with <name> already exists`

`GET` - will return the a JSON array listing all `diet`s
- Ports: `80`, `5002`
- Response:
    - Code: `200`
    - Content: `[ <diet JSON>, <diet JSON>, <diet JSON>, ...]`  
    If no records created, the array is empty: `[]`
---
### /diets/:name
`GET` - will return the the JSON representation of the `diet` with the given `name`.  
- Ports: `80`, `5002`
- URL Params (required):
    - `name: <string>` 
- Success Response:
    - Code: `200`
    - Content: `<diet JSON>`
- Error Response:
    - The diet `name` was not found:
        - Code: `404 Not Found`
        - Content: `Diet <name> not found`