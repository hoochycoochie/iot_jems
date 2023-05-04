create_topic:
	docker exec kafka  kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic new_csv_kafka_topic
delete_topic:
	docker exec kafka  kafka-topics.sh --delete --zookeeper zookeeper:2181  --topic new_csv_kafka_topic
compose:
	docker-compose up --build
volume_db:
	docker volume create mongo_volume

mongo:
	docker container run -d --name mongodb -p 27017:27017 -v mongo_volume:/data/db mongo:4.4

pyspark:
	docker container  run -d --name pyspark-notebook  --user root -e PASSWORD=amadou -e GRANT_SUDO=yes -p 8888:8888 jupyter/pyspark-notebook
