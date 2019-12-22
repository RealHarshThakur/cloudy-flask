# flask-restplus-app
This repo contains microservices implemented using Flask-restplus. 

# Setup
 Each directory would have detailed instructions about setting up the specific component. 
 
 Informatioin about generic files will be mentioned here.
 
 ## service.yaml
 To view the app locally we expose it from the minikube cluster to our local VM using a service.
 - kubectl create -f service.yaml
 
## ci.sh
This script is very useful to save bandwidth when you're developing locally. It pushes a local docker image to the minikube cluster by taking the name of the image as an argument. To utilise it move into the directory where your Dockerfile is in and type:
- "<Path>"/ci.sh <name of the docker image>

Goals of the web app is(Note: This is not a chronological sequence) :
- Have a database to store user data
- Create a database API for interaction with other services 
- Create a user service which performs general user actions along with authentication and authorization
- Have a task queue and message broker to send emails out 
- Containerize the application
- Kubernetize the application 
- Integrate cool CNCF projects in it

