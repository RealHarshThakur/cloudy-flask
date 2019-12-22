# flask-restplus-app
This repo contains microservices implemented using Flask-restplus. 

# Setup
 Each directory would have detailed instructions about setting up the specific component. 
 
 Informatioin about generic files will be mentioned here.
 
 ## service.yaml
 To view the app locally we expose it from the minikube cluster to our local VM using a service.
 - kubectl create -f service.yaml

Goals of the web app is(Note: This is not a chronological sequence) :
- Have a database to store user data
- Create a database API for interaction with other services 
- Create a user service which performs general user actions along with authentication and authorization
- Have a task queue and message broker to send emails out 
- Containerize the application
- Kubernetize the application 
- Integrate cool CNCF projects in it

