# Flask-MongoDB Application
_*This project was created back in a while(with documentation) in 10 days for an assignment. I'm not maintaining this project anymore_

An application that stores and retrieve json data via HTTP API. The endpoints list given below

<table>
 <th>
  <td>Name</td>
  <td>HTTP Method</td>
  <td>Endpoint</td>
  <td>Description</td>
 </th>
 <tr>
  <td>List</td>
  <td>GET</td>
  <td>/configs</td>
  <td>Lists available configuration in the server</td>
 </tr>
 </tr>
  <td>Create</td>
  <td>POST</td>
  <td>/configs</td>
  <td>Create/stores configuration in the server </td>
 </tr>
 <tr>
  <td>Get</td>
  <td>GET</td>
  <td>/configs/<config_name></td>
  <td>Fetches configuration details for a specific configuration</td>
 </tr>
 <tr>
  <td>Update</td>
  <td>PUT/PATCH</td>
  <td>/configs/<config_name></td>
  <td>Updates configuration for specific configuration</td>
 </tr>
  <tr>
  <td>Delete</td>
  <td>Delete</td>
  <td>/config/<config_name></td>
  <td>Delete a configuration</td>
 </tr>
  <tr>
  <td>Query</td>
  <td>GET</td>
  <td>/search?name=<config_name>&data.<key>.=<value></td>
  <td>Search configuration</td>
 </tr>
</table>

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
As we can see in above section, application to stores JSON data. We definitely can’t store data in files which we all knew “File System Storage” lacks ACID properties especially when we are serving data to multiple user. So, the best way to store data is storing it in DBMS. 
That brings up another question, which/what kind of database should solve our problem. If we look at our goal again, we want to store a JSON (configuration) which the size of JSON document is unknown or don’t want to put constraint on users to send only certain number of keys values pairs. But, if we choose to use traditional RDBMS programs, we have to define schema/table in DB. So, clearly we don’t want use SQL DBMS software like MySQL, Progress (NOTE: Recent versions of these software can supports NoSQL). One another problem or extra work in coding is we have to code to get keys values and write SQL to inject in tables.
By observing above problems of RDBMS, “NoSQL” got my attention which covers all drawbacks of RDBMS. I chose, “MongoDB” as backend to our application to store JSON. MongoDB is popular NoSQL DBMS, supports JSON document storage, can define constraints on data, support indexing and “Schema less”, etc.

### Frontend
An API that stores/fetches data from/in DB. I chose Flask to implement API. Flask is a Python framework designed to easy to use and light weight. 
After reviewing pro and cons of difference technologies to design backend and frontend, I chose below technologies/DB/framework with respective to their roles.

<table>
 <th>
 <td>Role</td>
 <td>Framework</td>
 </th>
 <td>
 <td>Frontend</td>
 <td>Flask</td>
 </td>
 <td>
 <td>Backend</td>
 <td>MongoDB</td>
 </td>
</table>

![alt text](http://image)

## Implementation
The API was implemented in Python 2.7 flask framework which communicates to MongoDB to store/fetch data accordingly with help of official python module from MongoDB “pymongo”. 
The API has capability of identify HTTP methods and performs actions according to it. The API validates the user input and send response as HTTP status code and text message which describes about issue in JSON format if there is any. If the user’s input is valid, the API store JSON document in DB (or fetch data from DB). 
In order to avoid malicious requests for “Query” endpoint which API might struck if user pass malicious urls, the application does regular expression on input query string and expected query string.

## Deployment
Our goal is to deploy application on Kubernetes cluster. Before that, we should do some tweaking to our application. As flask docs says “Flask’s built-in server is not suitable for production as it doesn’t scale well”. So, we should deploy flask application to WSGI server. We will use fully reliable HTTP server Apache to serve our application to end user with help of “mod_wsgi” which is an Apache module that implements a WSGI compliant interface for hosting Python based web applications on top of the Apache web server.

![alt text](http://image)

## Building Docker images
Before deploying our application in kubernetes, we need to build docker images and push docker image to hosting repository. Since we already identified frontend and backend, we can build a  docker image for frontend contains Apache webserver + flask application (HTTP API) and another for mongoDB. We will use quay.io to store our docker images (private repo). 
 
## Deployment on Kubernetes
Once docker image push to registry is complete. We can deploy application on K8s by using deployment manifest files that I provided along with this doc.
1.	Since we are going to deploy on “minikube” which is only for development. We are not using PV, PVC for MongoDB (PV and PVC are highly recommended in production). I have defined “EmptyDir” config which persistence of data is lifetime of pod.
2.	As we can see in manifest files, we mount/injects configuration via “secrets”/environmental variables. 

![alt text](http://image)
