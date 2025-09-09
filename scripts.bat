/* run local kafka container on 9092 */
/* to connect from container - need to create and connect to the same network
/* if need to connect from container inside docker to kafka: host=kafka, port=29092
/* if nees to connect from local to kafka on docker: host=localhost, port=9092 */
docker run -d --name kafka -p 9092:9092 -e KAFKA_NODE_ID=1 -e KAFKA_PROCESS_ROLES=broker,controller -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:29092,CONTROLLER://0.0.0.0:29093,PLAINTEXT_HOST://0.0.0.0:9092 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092 -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@localhost:29093 -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT -e KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 -e KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1 -e KAFKA_LOG_DIRS=/tmp/kraft-combined-logs apache/kafka:latest

docker network create kafka-net
docker network connect kafka-net kafka


cd  C:\Users\User\Desktop\Muazine


cd app\files_meta_pub
docker build -t david4554545/files_meta_pub .
docker run -d --name files_meta_pub --network kafka-net --volume C:\Users\User\Desktop\Muazine\podcasts:/app/podcasts david4554545/files_meta_pub

cd ..


cd  C:\Users\User\Desktop\Muazine
cd app\consume_and_persist
docker build -t david4554545/consume_and_persist .
docker run -d --name consume_and_persist --network kafka-net --volume C:\Users\User\Desktop\Muazine\podcasts:/app/podcasts david4554545/consume_and_persist

cd ..
cd stt
docker build -t david4554545/stt .
docker run -d --name stt --network kafka-net --volume C:\Users\User\Desktop\Muazine\podcasts:/app/podcasts david4554545/stt
