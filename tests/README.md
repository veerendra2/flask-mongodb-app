# Test Scripts & Internals
This page contains details on each endpoints, like what are the inputs to feed, possible output, response code, constraints and test script to validate the endpoint behaviors.
First we will see endpoints details and its test script for every endpoint.

`run.py` script which is a automated script to deploy app in K8s and **last we will see order of running tests scripts**.

## 2.` /configs` Endpoint (List: Method – GET)
Lists all available configs in DB. 
##### Test script
```
cd tests
./list_GET.py
```
Returns all configs on console

## 3. `/configs` Enpoint (Create: Method – POST)
API accepts below json format and store in DB on successful validation
```
{
	"name": "nova",
	"data": [
		{
			"key": "value2",
			"key2": "value2"
		}
	]
}
```
*NOTE: From now onward, we will refer the key “name” as config name or just “config”

In[ __init__.py](https://github.com/veerendra2/python-flask-mongodb-app/blob/master/app/myapp/http_api/__init__.py), the function [“validate_json_data”](https://github.com/veerendra2/python-flask-mongodb-app/blob/master/app/myapp/http_api/__init__.py#L19) checks input json data with below constraints
1. Should contain “name” key and value can be alphanumeric and _
2. Should contain “data” key and must contain array of dictionary 
3. DB is indexed on key “name”, so the “name” value should be unique

The function [“insert_doc”](https://github.com/veerendra2/python-flask-mongodb-app/blob/master/app/myapp/http_api/__init__.py#L44) in __init__.py is responsible for inserting the document in mongoDB
In __init__.py, [“convert_strings”](https://github.com/veerendra2/python-flask-mongodb-app/blob/master/app/myapp/http_api/__init__.py#L30) function convert all key values in JSON into string. This is useful while querying for key or config. Key value searching fails if datatype mismatches i.e the stored key value is in int and search key value in string which leads none results

##### Test Script
```
cd tests
./create_POST.py
```
Uses [“sample_data.json”](https://github.com/veerendra2/python-flask-mongodb-app/blob/master/tests/sample_data.json) file contains array of json objects which we are going to use in entire test procedure. [“create_POST.py”](https://github.com/veerendra2/python-flask-mongodb-app/blob/master/tests/create_POST.py) injects all json objects into DB via /config encpoint with POST method. For testing I made changes to some json objects to violate the constraints which we saw above. We can see script in action in below screenshot

![createPOST](https://raw.githubusercontent.com/veerendra2/python-flask-mongodb-app/master/images/create_post.jpg)

As we can see some json objects violated and gets error messages. We can also see HTTP response code.

## 4. `/configs/{name}` Enpoint (Create: Method – GET)
Returns configuration (JSON) of specified config name in URL, if config name exists in DB. [“get_document”](https://github.com/veerendra2/python-flask-mongodb-app/blob/master/app/myapp/http_api/__init__.py#L83) is responsible for the endpoint.

##### Test script
```
cd tests
./get_GET.py
```
In the tests directory, you can find 2 text files [“available_list.txt”](https://github.com/veerendra2/python-flask-mongodb-app/blob/master/tests/create_POST.py) which contains config names picked from “sample_data.json” and in the same way [“deleted_list.txt”](https://github.com/veerendra2/python-flask-mongodb-app/blob/master/tests/deleted_list.txt).

“deleted_list.txt” are delete config which are not exist in DB (NOTE: remove_DELETE.py uses this file and delete these configs. For now, just pretend these configs are not exists in DB)

“available_list.txt” contains the 10 configs are in DB

[get_GET.py](https://github.com/veerendra2/python-flask-mongodb-app/blob/master/tests/get_GET.py) uses these two files to fetch configs from DB. At time scripts using “deleted_list.txt”, the config name should fail which you can below screenshot. In the same way it should show success for “available_lists.txt”

![get_GET](https://raw.githubusercontent.com/veerendra2/python-flask-mongodb-app/master/images/get_get.png)

NOTE: At the end, we will see order of these script execution.

## 5. `/configs/{name}` Endpoint (Update: Method – PUT)
Updates config’s “data” i.e. the input json from user will overwrite for specified config name.  It uses “convert_strings” function to convert key value in input json like create endpoint and “validate_json_data” to validate input data. 
Accepts below json 
```
{
	"data": [
		{
			"key": "value2",
			"key2": "value2"
		}
	]
}
```
Test script
```
cd tests
./update_PUT.py
```
For this test, the script will pick randomly 2 json objects from “sample_data.json” and update 1st json’s “data” value with 2nd json’s “data” value.

![update_PUT](https://raw.githubusercontent.com/veerendra2/python-flask-mongodb-app/master/images/update_put.png)

Below screenshot gives insight on updating process. Also we can see the “modified_count” on successful update.

## 6. `/configs/{name}` Endpoint (Update: Method – DELETE)
Deletes specified configuration. [“delete_doc”](https://github.com/veerendra2/python-flask-mongodb-app/blob/master/app/myapp/http_api/__init__.py#L98) function in __init__.py is responsible for this functionality.
Test script
```
cd tests
./remove_DELETE.py
```
Uses “deleted_list.txt” config list to delete configs in DB.(Contains 10 config names)

![remove_DELETE](https://raw.githubusercontent.com/veerendra2/python-flask-mongodb-app/master/images/remove_delete.png)

It returns “deleted_count” as 1 on successful deletion

## 7. `/search?` Endpoint (Query: Method – GET)
Searches config with key value. Uses regular expression to validate the input URL and does the search operation in DB. We can perform search in two ways
```
TYPE1 - /search?name={config_name}&data.{key}={value}
TYPE2 - /search? data.{key}={value}
```
Returns all matched configs. [“query_doc”](https://github.com/veerendra2/python-flask-mongodb-app/blob/master/app/myapp/http_api/__init__.py#L131) is responsible for the endpoint. 
Test script
```
cd tests
./query_GET.py
```
Queries configs for “available_lists.txt” and “deleted_list.txt”. As we know the queries should fail for “deleted_lists.txt” configs and success for available_lists.txt

We can also query URL for type1 and type2 with their outputs.

![query_GET](https://raw.githubusercontent.com/veerendra2/python-flask-mongodb-app/master/images/query_get.png)

## 8.run.py
Automated script to perform deployment process in K8s. It does the following things
1. Checks docker/kuectl CLI/packages exists or not
2. Build docker images for frontend and backend 
3. Push docker images to registry(quay.io)
4. Creates image pull requests secrets in K8s
5. Launches application on K8s

NOTE:
* [run.py](https://github.com/veerendra2/python-flask-mongodb-app/blob/master/run.py) uses [run.cfg](https://github.com/veerendra2/python-flask-mongodb-app/blob/master/run.cfg) to gets configuration and modify/does accordingly
* I have a free and dummy quay.io which can push our docker images to private repos.(Specified credentials in run.cfg)
* run.py uses template manifests files in /k8s/manifests/ to generate actual manifest files.

#### Script in action

![Run1](https://raw.githubusercontent.com/veerendra2/python-flask-mongodb-app/master/images/run_1.png)

![Run2](https://raw.githubusercontent.com/veerendra2/python-flask-mongodb-app/master/images/run_2.png)


Once process is completed. Run “minikube ip > tests/ip”. Minikube ip shows ip of minikube cluster node. We need this IP to perform tests. 
In K8s manifest file, I have specified “NodePort” for frontend’s service and defined “NodePort” too. So, once pods are up, you can hit http://<minikube_IP>:32242/configs/

## 9. Recommended Configuration 

<table>
 <tr>
	 <td>OS</td><td>Ubuntu/ Any other Debian distros/ Linux</td>
 </tr>
  <tr>
	 <td>RAM</td><td>8 GB / Enough ram to run minikube cluster</td>
 </tr>
	
</table>

##### Packages/cluster

* minikube cluster should up and running
* docker (Use dependency_installer.py in miscellaneous directory to install it)
* requests python module

#### Test script order of execution

```
$ ./run.py
$ # once the process completed
$ minikube ip > tests/ip
$ cd tests
$ ./create_POST.py # Create Test
$ ./remove_DELETE.py # Delete Test
$ ./get_GET.py # Get List Test
$ ./query_GET.py # Query Test
$ ./update_PUT.py # Update Test
```
**NOTE: Please run the test script in above order.**


