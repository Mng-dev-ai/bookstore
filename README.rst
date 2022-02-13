Overview
--------
We have 3 docker containers:

    * **db**: runs the database
    * **api1**: runs the book store API server
    * **api2**: runs the count occurrences API server

- **db** is a mysql container, and **api1** and **api2** are Flask containers.
- **api1** and **api2** are both running on the same host, but they are running on different ports
- **api1** connects to **db** and **api2**.
- **api1** waits for **db** to start up.

Before we start **api1**,we run the following commands:

    * **flask db migrate**: reviews and edits the migration files
    * **flask db upgrade**: applies the migration files to the database
    * **flask init**: creates the dummy data from csv file in our database

Requirements
------------
* docker
* docker-compose

Usage
-----
.. code-block:: console

    $ docker-compose -f docker-compose.yml up

Configuration
-------------
Configuration is handled by environment variables, for development purpose you just need to update / add entries in .flaskenv file.

Using APISpec, Swagger, and ReDoc
-----------------------------------
This proejct comes with pre-configured APISpec and swagger endpoints. Using default configuration you have four endpoints available:

* `/swagger.json`: return OpenAPI specification file in json format
* `/swagger-ui`: Swagger UI configured to hit OpenAPI json file
* `/openapi.yaml`: return OpenAPI specification file in yaml format
* `/redoc-ui`: ReDoc UI configured to hit OpenAPI yaml file


Endpoints
---------
Open your browser and type http://localhost:5000/swagger-ui/ to see the swagger UI which has all the endpoints needed to test the API.

Testing
-------
To test the application you can use the following commands:

.. code-block:: console

    $ docker-compose -f docker-compose.yml up -d

    $ docker exec -it api1 bash -c "cd BookStore && tox -e test" 




