docker stop text_classifier
docker rm text_classifier
docker rmi david4554545/text_classifier

cd C:\Users\User\Desktop\Muazine\app\text_classifier

docker build -t david4554545/text_classifier .
docker run -d --name text_classifier --network muazine_proj_net david4554545/text_classifier
