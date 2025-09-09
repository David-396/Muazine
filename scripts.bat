/* run the Elasticsearch on 9200 */
/* to connect from container - need to create and connect to the same network
/* if need to connect from container inside docker to es: host=es, port=9200
/* if nees to connect from local to es on docker: host=localhost, port=9200 */
/* docker run -d --name es -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "ES_JAVA_OPTS=-Xms1g -Xmx1g" docker.elastic.co/elasticsearch/elasticsearch:8.15.0


/* kibana - es ui - connect to the same network*/
/* docker network create elk-network
/* docker network connect elk-network es
/* docker run -d --name kibana --net elk-network -p 5601:5601 -e "ELASTICSEARCH_HOSTS=http://elasticsearch:9200" docker.elastic.co/kibana/kibana:8.15.0

/* run local mongo_db on port 27017 */
/* to connect from container - need to create and connect to the same network
/* if need to connect from container inside docker to mongo_db: host=mongo_db, port=27017, user=root, password=pass
/* if nees to connect from local to mongo on docker: host=localhost, port=27017, user=root, password=pass */
/* docker run --name mongo_db -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=pass -d mongodb/mongodb-community-server:latest

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

