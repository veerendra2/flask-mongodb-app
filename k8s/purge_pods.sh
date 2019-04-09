#!/usr/bin/env bash

kubectl delete -f mongodb_secrets.yml
kubectl delete -f mongoDB.yml
kubectl delete -f http_service.yml
kubectl delete secret regcred