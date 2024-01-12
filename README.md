# FeedMe Server

**🍜🥦 Nourishment RESTful API - Providing High Availability**  
Check out the [API documentation](/api.md)  
<img width="612" alt="FeedMe-HA-Architecture" src="https://github.com/OferPeery/feedme-high-availability/assets/90853508/ea903b1f-db15-40be-bd20-bb2383ba0a32">

## Versions
This application has 2 versions, each emphasizing a different aspect of software engineering in the cloud:
- HA - High Availability version (this)
- CI - Continuous Integration version (will be published soon)

## Design & Tech 
Architectural styles and implementation technologies:
* RESTful APIs - Python and Flask
* Microservices - Docker Containers and Docker Compose
* High Availability - Docker Compose, MongoDB
* Reverse Proxy / Load Balancer - NGINX  
* OOP - Python

This project practices the concepts of building loosely coupled, abstract, robust and distributed systems to achive separation of concerns, enabling independent evolving and an improved maintainability of each component, as well as minimizing potential downtime damage thanks to this seperation and redundancy, resulting in high availability. 

## Prerequisites

1. You need [Docker](https://www.docker.com/products/docker-desktop/) installed to run the server-app's microservices locally on Docker Containers.
2. You need an `API-key` of your own for fetching data from [api-ninjas](api-ninjas.com/api/nutrition).
    - Watch the [demo video](https://www.youtube.com/watch?v=QPTVTNqupr0) for creating your own `API-key`.
    - Update `/meal-server/dish_ninja_creator.py` to include your `api-key`:
        ```
        class DishNinjaCreator:
            def __init__(self):
                self.api_key = 'YOUR-API-KEY'
        ```
    - 50,000 API calls per month are free - https://api-ninjas.com/pricing
    - Read the [api-ninjas documentation](https://api-ninjas.com/api/nutrition)  

## Install & Run

Run the following command in your terminal to build all the Docker images in this project and run them on containers:
```
docker compose -f docker-compose.yml up
```
Now all the microservices up and running, and you can use the API according to the [documentation](/api.md).

## Test High Availability
**This project includes:**
1. **Disaster Recovery**  
The 3 microservices `meal-service`, `diet-service` and `reverse` are implemented with a disaster recovery mechanism such that they restart immediately, and in the correct dependency order after a failure occurs.  
2. **Persistent Data**  
Is implemented thanks to the `mongo` microservice which uses docker's volume to store the data stored in the `mongodb` database.
---
**Test:**  
In a new terminal - run the following commands to kill a service:
1. See the list of currently running containers:
    ```
    docker ps
    ```
2. Copy the container-hash of the container that you'd like to test.
3. Open a `zsh` terminal inside this container (replace the `<container-hash>` parameter with your own):
    ```
    docker exec -it <container-hash> /bin/sh
    ```
4. Kill the main process inside the container's zsh terminal:
    ```
    kill 1
    ```
---

**Results:** 
1.  Check if the "STATUS" column of the tested container has: "Up about `<x>` seconds" (or so) - to see if it restarted
    ```
    docker ps
    ```
2. Send a `GET` request to the resource(s) correspond(s) to the tested service.  
Notice that the records that has been previously inserted to the server are still there and accessible.

## Stop
1. **Stop and remove the containers and/or images:**  
    choose one of the 3 options:
    - Stop and remove all the **containers** created by the docker-compose up command:
        ```
        docker compose -f docker-compose.yml down
        ```
    - Stop and remove **containers and images** built **LOCALLY ONLY** with the specified docker-compose up command (i.e. without `mongo` service) to save future re-download:
        ```
        docker compose -f docker-compose.yml down --rmi local
        ```
    - Stop and remove **ALL containers and images** built with the specified docker-compose up command:
        ```
        docker compose -f docker-compose.yml down --rmi all
        ```
2. **Remove the associated volumes (optional):**  
    List all Docker volumes, and then delete the specific 2 volumes associated with the application:
    ```
    docker volume ls
    docker volume rm <volume_name1>
    docker volume rm <volume_name2>
    ``` 

## Author

- Ofer Peery - peryofer7@gmail.com

## License

This application was developed as part of the Cloud Computing and Software Engineering Course, lectured by Dr. Danny Yellin in Reichman University.  
This project is licensed under the MIT License (see License.md for more details).  
