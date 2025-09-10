docker stop stt
docker rm stt
docker rmi david4554545/stt

cd C:\Users\User\Desktop\Muazine\app\stt

docker build -t david4554545/stt .
docker run -d --name stt --network muazine_proj_net --volume C:\Users\User\Desktop\Muazine\podcasts:/app/podcasts david4554545/stt
