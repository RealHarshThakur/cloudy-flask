# Cloudy-Flask
Started out this project to learn about developing and deploying microservices using Cloud native projects. 
This repo contains microservices implemented using Python's Flask-restplus to create backend services by taking a cloud native approach. The project starts out with the application running on Docker and later branches out to running on Kubernetes. 


# About the application 
# Note: Each folder contains it's microservice where they have a detailed info in their README.
## Database choice: MongoDB
Application is backed by Mongodb which is exposed by a REST API. 
## Backend services: 
- Database API: A single database API to expose the MongoDB for CRUD operations pertaining to user actions without access control.
- User Service: Contains JWT auth and authorization code for user actions. Look at the README for more info.
- Email service: Would send out emails to registered users.
  - Would use Celery and Redis as task queue and message broker to accomplish this.
  
# Current Progress
- Implemented the Database API. 
- Implemented the Users API
- Implemented the Email API
- Service Discovery is done natively by Kubernetes's CoreDNS

# Setup
 Each directory would have detailed instructions about setting up the specific component. 
 
 Informatioin about generic files will be mentioned here.
 
 ## service.yaml
 To view the app locally we expose it from the minikube cluster to our local VM using a service.
 - kubectl create -f service.yaml
 
## ci.sh
This script is very useful to save bandwidth when you're developing locally. It pushes a local docker image to the minikube cluster by taking the name of the image as an argument. To utilise it move into the directory where your Dockerfile is in and type:
- \<Path>/ci.sh \<name of the docker image> \<name of the deployment>

Take a look at this blog post about how I develop apps in Kubernetes:
https://medium.com/harsh-thakur/developing-apps-locally-on-kubernetes-eee7600ee0f8
