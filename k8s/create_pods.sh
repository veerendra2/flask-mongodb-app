kubectl create secret docker-registry regcred --docker-server=https://quay.io --docker-username=veeru553 --docker-password=Qwerty@123 --docker-email=jemamo@tempcloud.info
kubectl create -f mongodb_secrets.yml
kubectl create -f mongoDB.yml
kubectl create -f http_service.yml
