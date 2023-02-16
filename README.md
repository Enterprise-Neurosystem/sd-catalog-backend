# sd-catalog-backend
This repository contains a Python implementation of a catalog of self-describing assets. It is being developed by the members of the Central Intelligence Platform Working Group. To learn more about the group and join, please visit the following link:
https://github.com/Enterprise-Neurosystem/central_intelligence_platform_meetings

## Getting Started
### Install MongoDB and Python
 To use the system locally, you need to have [MongoDB](https://www.mongodb.com/try/download/community) installed and accessible. 

  The URL of the MongoDB instance to use needs to be defined in the instance/config.py file.

  Make sure you have python >= 3.9 installed on your system.

### Build using Poerty
 You need to install [poetry](https://python-poetry.org/) to install dependencies and build the project.

```console
poetry install
```

This will create a virtual environment for you and your code will run in the virtual environment

### Run the project
```console
export FLASK_APP=catalog
poetry run flask run
```
The above commands will work for zsh and Linux. If you are using another shell or windows, export the variable appropriately. 

During development, if you want to debug set the debug flag.

```console
export FLASK_DEBUG=1
```
The difference between the two is that exceptions are exposed in detail in development mode.

Once the server is running, you can access the REST API for self-describing entries. 
In development mode, the default server is at http://127.0.0.1:5000. The REST API is accessible via the prefix http://127.0.0.1:5000/sda. 
The user management console is located at http://127.0.0.1:5000/user/index.

## Running the Application with Docker

The application can also be run using containers. You need to have the ability to build images locally and run them as containers. The current version has been tested using Docker Desktop.

To bring up the application using Docker Compose:

```console
$ cd sd-catalog-backend

$ docker-compose up -d --build
```
This will bring up two containers 
+ sd-catalog-backend - containing the application logic and an embedded sqlite datastore for user management
+ mongodb - managing the self describing catalogue entries

The swagger documentation is avalable at http://127.0.0.1:5000/apispec/

Below are the available APIs. 

```console
$ http localhost:5000/user/list

HTTP/1.1 200 OK
Connection: close
Content-Length: 559
Content-Type: text/html; charset=utf-8
Date: Sat, 06 Aug 2022 00:45:53 GMT
Server: Werkzeug/2.2.1 Python/3.9.13

<!doctype html>
<title>List All Users  -  Self Describing Assets Catalog </title>
<link rel="stylesheet" href="/static/style.css">
<nav>
  <h1>Self Describing Assets Catalog </a></h1>
  <ul>

    <h>  </h>

  </ul>
</nav>

<section class="content">
  <header>

  <h1>List All Users </h1>

  </header>



  <h3>List of Registered Users </h3>
 <table border=5>
 <thead>
 <td>ID</td>
 <td>Name</td>
 <td>Email</td>
 <td>Delete</td>
 </thead>

 </table>
 <p> <a href=/user/index> Back to User Management </a> </p>

</section>

$ http POST localhost:5000/sda/create data_uri=https://www.ibm.com scope=global data_type=cfr metadata=nil

HTTP/1.1 200 OK
Connection: close
Content-Length: 128
Content-Type: text/html; charset=utf-8
Date: Sat, 06 Aug 2022 00:14:48 GMT
Server: Werkzeug/2.2.1 Python/3.9.13

{
    "_id": "62edb278f37e9ebaa2c1b0ae",
    "data_type": "cfr",
    "data_uri": "https://www.ibm.com",
    "metadata": "nil",
    "scope": "global"
}

$ http POST localhost:5000/sda/list

HTTP/1.1 200 OK
Connection: close
Content-Length: 130
Content-Type: text/html; charset=utf-8
Date: Sat, 06 Aug 2022 00:14:54 GMT
Server: Werkzeug/2.2.1 Python/3.9.13

{{"_id": "62edb278f37e9ebaa2c1b0ae", "data_uri": "https://www.ibm.com", "scope": "global", "data_type": "cfr", "metadata": "nil"}}

$ http POST localhost:5000/sda/retrieve _id=62edb278f37e9ebaa2c1b0ae

HTTP/1.1 200 OK
Connection: close
Content-Length: 128
Content-Type: text/html; charset=utf-8
Date: Sat, 06 Aug 2022 00:18:42 GMT
Server: Werkzeug/2.2.1 Python/3.9.13

{
    "_id": "62edb278f37e9ebaa2c1b0ae",
    "data_type": "cfr",
    "data_uri": "https://www.ibm.com",
    "metadata": "nil",
    "scope": "global"
}
```
<hr>
