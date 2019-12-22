This folder contains all the code and configuration files to get the mongodb database and the flask API to interact with the database, up and running.

If you have a kubernetes cluster, you can start the API by running:
- kubectl create -f database.yaml 

To have the mongodb instance up, you can run 
- kubectl create -f mongodb

If you face issues interacting with the db, get a shell on the db pod and create a db named "users". 
- kubectl exec -it <name of the mongodb pod> mongo
- use users

I have provided the Dockerfile which you can build locally and push to your minikube cluster using ci.sh(in the root directory of the repo) by giving it a custom name.



