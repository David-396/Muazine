docker stop files_meta_pub
docker rm files_meta_pub
docker rmi david4554545/files_meta_pub

cd C:\Users\User\Desktop\Muazine\app\files_meta_pub

docker build -t david4554545/files_meta_pub .
docker run -d --name files_meta_pub --network muazine_proj_net --volume C:\Users\User\Desktop\Muazine\podcasts:/app/podcasts david4554545/files_meta_pub
