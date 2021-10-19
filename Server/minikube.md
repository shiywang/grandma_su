# How to deploy on top of Kubernetes

Make sure you have kubernetes cluster pre-intalled


```










```



## Minikube and docker-compose

```
minikube start --insecure-registry "10.0.0.0/24"

minikube dashboard

minikube addons enable registry

docker-compose run api python manage.py migrate

docker-compose run api python care_api/manage.py createsuperuser

```

## How to run stimulation tests

after succesfully configed all the services.

```
cd Test/Server_Test/

rm data_store/datastore.txt

python3 test1.py 5
```
