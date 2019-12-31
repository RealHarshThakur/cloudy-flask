# flask-restplus-app
Started out this project to learn about developing and deploying microservices using Cloud native projects. 
This repo contains microservices implemented using Python's Flask-restplus to create backend services by taking a cloud native approach. The project starts out with the application running on Docker and later branches out to running on Kubernetes. 


# About the application 
## Database choice: MongoDB
Application is backed by Mongodb which is exposed by a REST API. 
## Backend services: 
- Database API: To expose the MongoDB for CRUD operations.
- User Service: Would have all the logic for user managment like register, login, etc.
- Email service: Would send out emails to registered users.
  - Would use Celery and Redis as task queue and message broker to accomplish this.
  
# Current Progress
- Implemented the Database API. 
- App can run in Kubernetes
- Service Discovery is done natively by Kubernetes(Future version would use a service mesh like Istio/Consul)

# Setup
 Each directory would have detailed instructions about setting up the specific component. 
 
 Informatioin about generic files will be mentioned here.
 
 ## service.yaml
 To view the app locally we expose it from the minikube cluster to our local VM using a service.
 - kubectl create -f service.yaml
 
## ci.sh
This script is very useful to save bandwidth when you're developing locally. It pushes a local docker image to the minikube cluster by taking the name of the image as an argument. To utilise it move into the directory where your Dockerfile is in and type:
- \<Path>/ci.sh \<name of the docker image>

# Goals of the web app is(Note: This is not a chronological sequence) :
- Have a database to store user data
- Create a database API for interaction with other services 
- Create a user service which performs general user actions along with authentication and authorization
- Have a task queue and message broker to send emails out 
- Containerize the application
- Kubernetize the application 
- Integrate cool CNCF projects in it

