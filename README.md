# sd-catalog-backend
A python implementation of catalog of self-describing assets

In order to use the system, you need to have mongo database accessible. 
You can install the mongo db from https://www.mongodb.com/try/download/community

The URL of the mongodb to use needs to be defined in the instance/config.py file 

To run the system after proper configuration, use the following shell commands from the directory containing catalog folder

```console
export FLASK_APP=catalog
flask run
```
The above commands will work for zsh and Linux. If you are using another shell or windows, export the variable appropriately. 

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

