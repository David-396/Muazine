docker stop consume_and_persist
docker rm consume_and_persist
docker rmi david4554545/consume_and_persist

cd  C:\Users\User\Desktop\Muazine\app\consume_and_persist

docker build -t david4554545/consume_and_persist .
docker run -d --name consume_and_persist --network muazine_proj_net --volume C:\Users\User\Desktop\Muazine\podcasts:/app/podcasts david4554545/consume_and_persist
