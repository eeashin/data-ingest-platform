#!/bin/bash
# This is a Unix-style bash script
set -e
trap 'echo "An error occurred. Exiting..."; exit 1;' ERR
echo "Downloading Kafka 3.0.0..."
curl -O https://archive.apache.org/dist/kafka/3.0.0/kafka_2.13-3.0.0.tgz
sleep 5
tar xzf kafka_2.13-3.0.0.tgz
mv kafka_2.13-3.0.0 kafka-cluster
sleep 5
rm -rf kafka_2.13-3.0.0.tgz
cp -f server* kafka-cluster/config
sleep 5
echo "Starting Zookeeper server..."
kafka-cluster/bin/zookeeper-server-start.sh kafka-cluster/config/zookeeper.properties
echo "Zookeeper server Running..."
