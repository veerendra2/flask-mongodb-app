[![GitHub issues](https://img.shields.io/maintenance/no/2019.svg?style=plastic)](https://img.shields.io/maintenance/no/2019.svg?style=plastic)
[![GitHub forks](https://img.shields.io/github/forks/veerendra2/python-flask-mongodb-app.svg)](https://github.com/veerendra2/python-flask-mongodb-app/network)
[![GitHub stars](https://img.shields.io/github/stars/veerendra2/python-flask-mongodb-app.svg)](https://github.com/veerendra2/python-flask-mongodb-app/stargazers)
[![GitHub license](https://img.shields.io/badge/license-Apache%202-blue.svg)](https://github.com/veerendra2/python-flask-mongodb-app/master/LICENSE)
# Python-Flask-MongoDB Application
_*This project(with documentation) was created back in a while in 10 days for an assignment. Right now I'm not maintaining this project anymore._ :pray: 

_Heads-up before you use/look into the code_:warning:
* _I didn't know anything about MonogoDB or Flask framework at time I started the project._
* _I'm not a web devloper._

### Delopy on Kubernetes
You can use ready made K8s spec file in [k8s-ready-spec-files](https://github.com/veerendra2/python-flask-mongodb-app/tree/master/k8s-ready-spec-files) directory which I pushed the docker images to my quay.io account.(Modify spec files if you need)
```
$ git clone https://github.com/veerendra2/python-flask-mongodb-app.git
$ cd python-flask-mongodb-app/k8s-ready-spec-files
$ kubectl create -f k8s_mongodb_secrets.yml
$ kubectl create -f k8s_http_service.yml
$ kubectl create -f k8s_mongoDB.yml
```
Or you can build your own by running `run.py`(More info in [tests](https://github.com/veerendra2/python-flask-mongodb-app/tree/master/tests) directory)


# Introduction
A simple application that stores and retrieve json data via HTTP API. The endpoints list given below

| Name        | HTTP Method | Endpoint                                         | Description  |
| ----------- |:----------- | :------------------------------------------------| :------------|
| List        | GET         | `/configs`                                       | Lists available configuration in the server |
| Create      | POST        | `/configs`                                       |   Create/stores configuration in the server  |
| Get         | GET         | `/configs/<config_name>`                         |    Fetches configuration details for a specific configuration |
| Update      | PUT/PATCH   | `/configs/<config_name>`                         | Updates configuration for specific configuration |
| Delete      | DELETE      | `/configs/<config_name>`                         |   Delete a configuration   |
| Get         | GET         | `/search?name=<config_name>&data.<key>.=<value>` |  Search configuration  |


#### Configuration(Json Data) Schema Structure
```
[
 {
   "name": <unique_name>,
   "data": [
      {
        <key>: <value>
        <ke2>:<value>
      }
    ]
 }
]
```
#### Schema Example
```
[
  {
    "name": "Mckinney",
    "data": [
      {
        "id": 4608,
        "app_name": "cupidatat",
        "isActive": true
      },
      {
        "id": 2678,
        "app_name": "tempor",
        "isActive": true
      },
      {
        "id": 4114,
        "app_name": "adipisicing",
        "isActive": true
      }
    ]
  }
]
```

## Design
### Backend
As we can see, we want to develop application that stores JSON data. We definitely can’t store data in files which we all knew "File System Storage" lacks `ACID` properties especially when we are serving data to multiple user. So, the best way to store data is storing it in DBMS. 

That brings up another question, what kind of database should solve our problem. If we look at our goal again, we want to store a JSON (configuration) which the size of JSON document is unknown or don’t want to put constraint on users to send only certain number of keys values pairs. But, if we choose to use traditional RDBMS programs, we have to define schema/table in DB. So, clearly we don’t want use SQL DBMS software like MySQL, Progress (NOTE: Recent versions of these software can supports NoSQL). One another problem or extra work in coding is we have to code to get keys-values and write SQL to inject in tables.

By observing above problems, "NoSQL" got my attention which covers all drawbacks of RDBMS. I chose, ["MongoDB"](https://www.mongodb.com/) as a backend to our application to store JSON. MongoDB is popular NoSQL DBMS, supports JSON document storage, define constraints on data, support indexing and "schema less", etc.

### Frontend
An API that stores/fetches data from/in DB. I chose Flask to implement API. Flask is a Python framework designed to easy to use and light weight. 
After reviewing pro and cons of difference technologies to design backend and frontend, I chose below technologies/DB/framework with respective to their roles.

| Role        | Framework | 
| ----------- |:----------| 
| Frontend    | Flask     |
| Backend     | MongoDB   |


<img src="https://raw.githubusercontent.com/veerendra2/python-flask-mongodb-app/master/images/front_back_arch.png" width="500" height="100" />

## Implementation
The API was implemented in Python 2.7 flask framework which communicates to MongoDB to store/fetch data accordingly with help of official python module from MongoDB “pymongo”. 

The API has capability of identify HTTP methods and performs actions according to it. The API validates the user input and sends response back to user as HTTP status code and text message. If the user’s input is valid, the API store JSON document in DB (or fetch data from DB). 

In order to avoid malicious requests for “Query” endpoint which API might struck if user pass malicious urls, the application does regular expression on input query string and expected query string.

## Deployment
Our goal is to deploy application on Kubernetes cluster. Before that, we should do some tweaking to our application. As flask docs says "Flask’s built-in server is not suitable for production as it doesn’t scale well". So, we should deploy flask application to WSGI server. We will use fully reliable HTTP server Apache to serve our application to end user with help of “mod_wsgi” which is an Apache module that implements a WSGI compliant interface for hosting Python based web applications on top of the Apache web server.

<img src="https://raw.githubusercontent.com/veerendra2/python-flask-mongodb-app/master/images/web_server.png" width="500" height="200" />

### Building Docker images
Before deploying our application on kubernetes, we need to build docker images and push docker image to hosting repository. Since we already identified frontend and backend, we can build a  docker image for frontend contains Apache webserver + flask application (HTTP API) and another for mongoDB. We will use quay.io to store our docker images (private repo). 
 
### Deployment on Kubernetes
Once docker image push to registry is complete. We can deploy application on K8s by using deployment manifest files that I provided along with this doc.
1.	Since we are going to deploy on “minikube” which is only for development. We are not using PV, PVC for MongoDB (PV and PVC are highly recommended in production). I have defined “EmptyDir” config which persistence of data is lifetime of pod.
2.	As we can see in manifest files, we are mounting/injecting configuration via “secrets”/environmental variables. 

<img src="https://raw.githubusercontent.com/veerendra2/python-flask-mongodb-app/master/images/k8s_deployment.PNG" width="500" height="200" />

_*Check [`tests`](https://github.com/veerendra2/python-flask-mongodb-app/tree/master/tests) directory for more info._
