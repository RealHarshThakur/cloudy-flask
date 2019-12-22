docker build -t $1 .
docker save $1 |(eval $(minikube docker-env)&& docker load)
kubectl set image deployment $1
