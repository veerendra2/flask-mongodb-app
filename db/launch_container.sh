#!/usr/bin/env bash
sudo docker run -it -d -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=sigma MONGO_INITDB_ROOT_PASSWORD=Phief3me -e mymongodb