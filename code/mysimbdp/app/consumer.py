from confluent_kafka import Consumer
import argparse
import json
import time
from pymongo import MongoClient
from datetime import datetime
import os

KAFKA_BOOTSTRAP_SERVER = "localhost:9092"

client = MongoClient('mongodb://admin:admin@127.0.0.1:30000/admin?authSource=admin')#('mongodb://localhost:27017/')

db = client.airbnb
col = db.reviews
batch_size = 1000

def process_message(msg, message_buffer, batch_size=batch_size):
    """
    Process a message
    """
    if msg.error():
        print(f'Consumer error: {msg.error()}')
        return
    json_value = json.loads(msg.value().decode('utf-8'))
    print(f'Received message: {json_value}')
    message_buffer.append(json_value)
    if len(message_buffer) >= batch_size:
        col.insert_many(message_buffer)
        message_buffer.clear()

def get_mongo_performance_metrics(mongo_log):
    server_status = db.command("serverStatus")
    
    with open(mongo_log, 'a') as mongo_log:
        mongo_log.write(f"Connections: {server_status['connections']}\n")
        mongo_log.write(f"Memory Usage: {server_status['mem']}\n")
        mongo_log.write(f"Opcounters: {server_status['opcounters']}\n")
        mongo_log.write(f"Network: {server_status['network']}\n")

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--topic', help='kafka topic')
    parser.add_argument('-g', '--consumer_group', help='kafka topic')
    parser.add_argument('-n', '--num_consumers', help='number of consumers to run')
    args = parser.parse_args()



    # start multiple consumers
    num_consumers = int(args.num_consumers)
    kafka_consumers = [
        Consumer({
            'bootstrap.servers': KAFKA_BOOTSTRAP_SERVER,
            'group.id': args.consumer_group,
        }) for i in range(num_consumers)
    ]

    for consumer in kafka_consumers:
        consumer.subscribe([args.topic])
    running = True
    last_message_time = time.time()

    try:
        start_time = time.monotonic()
        message_buffer = []
        while running:
            for consumer in kafka_consumers:
                # poll for messages and process them one by one
                msg = consumer.poll(0)
                if msg is not None:
                    process_message(msg, message_buffer)
                    last_message_time = time.time()
                else:
                    time.sleep(1)
            elapsed_time = time.time() - last_message_time
            if elapsed_time >= 60:
                print("No messages received for 1 minute. Stopping consumer.")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                mongo_log_path = os.path.join(os.path.dirname(__file__), '../../../logs', f'mongo_log_{timestamp}.txt')
                get_mongo_performance_metrics(mongo_log_path) 
                running = False
        # insert remaining messages
        if message_buffer:
            col.insert_many(message_buffer)
    except KeyboardInterrupt:
        pass
    finally:
        for consumer in kafka_consumers:
            consumer.close()

    # calculate and print execution time
    end_time = time.monotonic()
    total_rows = col.count_documents({})
    execution_time = end_time - (start_time - 60)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    consumer_log_path = os.path.join(os.path.dirname(__file__), '../../../logs', f'consumer_log_{timestamp}.txt')
    
    with open(consumer_log_path, 'a') as consumer_log:
        consumer_log.write(f'Kafka topic: {args.topic}\n')
        consumer_log.write(f'Kafka consumer group: {args.consumer_group}\n')
        consumer_log.write(f'Number of consumers: {num_consumers}\n')
        consumer_log.write(f'batch size: {batch_size}\n')
        consumer_log.write(f"Total {total_rows} rows saved\n")
        consumer_log.write(f"Execution time: {execution_time/60:.2f} minutes\n")
        consumer_log.write(f"Rows per second: {total_rows/execution_time:.2f}\n")
