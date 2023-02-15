# sd-catalog-backend
This code is being developed by the members of Central Intelligence Platfrom Working Group. For more details and to join
the group please refer to: https://github.com/Enterprise-Neurosystem/central_intelligence_platform_meetings

A python implementation of catalog of self-describing assets

In order to use the system locally, you need to have mongo database accessible. 
You can install the mongo db from https://www.mongodb.com/try/download/community

The URL of the mongodb to use needs to be defined in the instance/config.py file 

To run the system after proper configuration, use the following shell commands from the directory containing catalog
folder

```console
export FLASK_APP=catalog
flask run
```
The above commands will work for zsh and Linux. If you are using another shell or windows, export the variable
appropriately. 

During development, use the following commands
```console
export FLASK_APP=catalog
export FLASK_ENV=development
flask run
```
The difference between the two is that exceptions are exposed in detail in development mode

Once the server is running, you can access the REST API for self-describing entries. 
In the development mode, the default server is at  http://127.0.0.1:5000.
The REST API is accessible via http://127.0.0.1:5000/sda prefix 
The user management console is at http://127.0.0.1:5000/user/index 

<hr>

The application can also be run using containers. You need to have the ability to build images locally and run them as
containers. The current version has been tested using Docker desktop.

To bring up the application using docker compose
```console
$ cd sd-catalog-backend

$ docker-compose up -d --build 

or 

$ docker-compose up --build
```
This will bring up two containers 
+ sd-catalog-backend - containing the application logic and an embedded sqlite datastore for user management
+ mongodb - managing the self describing catalogue entries

To test the application, use POSTMAN, [SWAGGER](http://127.0.0.1:5000/apispec/#/), curl commands or any other client
like httpie.

Using curl commands

* **Get all the Assets published in the catalog**

```console
$ curl -X 'GET' \
  'http://127.0.0.1:5000/sda/list' \
  -H 'accept: application/json'
```

_Response body_

```console
[
  {
    "_id": "63e549bb8bcb8d6c5b2b948b",
    "data_type": "1",
    "data_uri": "data_uri",
    "metadata": {
      "date_created": "2023-02-06T02:39:15",
      "date_updated": "2023-02-06T02:39:15",
      "name": "test"
    },
    "scope": "com.ibm.aot.eng"
  },
  {
    "_id": "63e54a548fc3a976865add29",
    "data_type": "1",
    "data_uri": "data_uri",
    "metadata": {
      "date_created": "2023-02-06T02:39:15",
      "date_updated": "2023-02-06T02:39:15",
      "name": "test"
    },
    "scope": "com.ibm.aot.eng"
  }
]
```

* **Publish an asset to the catalog**

```console
$ curl -X 'POST' \
  'http://127.0.0.1:5000/sda/create' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "data_type": "1",
  "data_uri": "data_uri",
  "metadata": {
    "name": "test",
    "date_created": "2023-02-06T02:39:15",
    "date_updated": "2023-02-06T02:39:15"
  },
  "scope": "com.ibm.aot.eng"
}'
```
	
_Response body_

```console
{
  "_id": "63ed5b84ca55ee384494b3a7",
  "data_type": "1",
  "data_uri": "data_uri",
  "metadata": {
    "date_created": "2023-02-06T02:39:15",
    "date_updated": "2023-02-06T02:39:15",
    "name": "test"
  },
  "scope": "com.ibm.aot.eng"
}
```

* **Retrieve a specific asset from the catalog**

```console
$ {
  "_id": "63ed5b84ca55ee384494b3a7",
  "data_type": "1",
  "data_uri": "data_uri",
  "metadata": {
    "date_created": "2023-02-06T02:39:15",
    "date_updated": "2023-02-06T02:39:15",
    "name": "test"
  },
  "scope": "com.ibm.aot.eng"
}
```

_Response body_

```console
{
  "_id": "63ed5b84ca55ee384494b3a7",
  "data_type": "1",
  "data_uri": "data_uri",
  "metadata": {
    "date_created": "2023-02-06T02:39:15",
    "date_updated": "2023-02-06T02:39:15",
    "name": "test"
  },
  "scope": "com.ibm.aot.eng"
}
```

* **Update a specific asset in the catalog**

```console
$ curl -X 'PUT' \
  'http://127.0.0.1:5000/sda/update/63ed5b84ca55ee384494b3a7' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "data_type": "3",
  "data_uri": "data_uri_update"
}'
```

_Response body_

```console
{
  "_id": "63ed5b84ca55ee384494b3a7",
  "data_type": "3",
  "data_uri": "data_uri_update",
  "metadata": {
    "date_created": "2023-02-06T02:39:15",
    "date_updated": "2023-02-06T02:39:15",
    "name": "test"
  },
  "scope": "com.ibm.aot.eng"
}
```

* **Delete a specific asset from the catalog**

```console
$ curl -X 'DELETE' \
  'http://127.0.0.1:5000/sda/delete/63ed5b84ca55ee384494b3a7' \
  -H 'accept: */*'
```

_Response body_

```console
"Asset deleted successfully!"
```

<hr>

To update the application during development you need to use the following commands to bring the app down and remove the
backend volume:
```console
$ docker-compose down
Removing sd-catalog-backend ... done
Removing mongodb            ... done
Removing network sd-catalog-backend_backend
Removing network sd-catalog-backend_frontend

$ docker volume ls

$ docker volume rm sd-catalog-backend_appdata
```