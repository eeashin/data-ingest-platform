import argparse
from confluent_kafka import Producer
import pandas as pd
import json
import time
from datetime import datetime
import os

def datetime_converter(dt):
    if isinstance(dt, datetime.datetime):
        return dt.__str__()

def kafka_delivery_error(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')

KAFKA_BOOTSTRAP_SERVER = "localhost:9092"


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', help='Input file')
    parser.add_argument('-c', '--chunksize', help='chunk size for big file')
    parser.add_argument('-s', '--sleeptime', help='sleep time in second')
    parser.add_argument('-t', '--topic', help='kafka topic')
    args = parser.parse_args()

    # Load input data
    INPUT_DATA_FILE = args.input_file
    chunksize = int(args.chunksize)
    sleeptime = int(args.sleeptime)
    KAFKA_TOPIC = args.topic

    input_data = pd.read_csv(INPUT_DATA_FILE, iterator=True, chunksize=chunksize)
    kafka_producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVER})
    
    row_count = 0 # Initialize row count to zero
    start_time = time.time() # Record start time before processing first row
    
    for chunk_data in input_data:
        # Process each chunk
        chunk = chunk_data.dropna()
        for index, row in chunk.iterrows():
            # Send each row to Kafka as a separate message in JSON format
            json_data = json.dumps(row.to_dict(), default=datetime_converter)
            print(f'DEBUG: Send {json_data} to Kafka')
            kafka_producer.produce(KAFKA_TOPIC, json_data.encode('utf-8'), callback=kafka_delivery_error)
            kafka_producer.poll(0)
            row_count += 1 # Increment row count for each row processed
        # Print row count after processing each chunk
        print(f'{row_count} rows processed so far')
        # Sleep between chunks
        time.sleep(sleeptime)

    kafka_producer.flush()
    end_time = time.time() # Record end time after processing all rows
    elapsed_time = end_time - start_time
    os.remove(INPUT_DATA_FILE)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    producer_log_path = os.path.join(os.path.dirname(__file__), '../../../logs', f'producer_log_{timestamp}.txt')

    with open(producer_log_path, 'a') as producer_log:
        producer_log.write(f'Kafka topic: {KAFKA_TOPIC}\n')
        producer_log.write(f'Producer sleep time: {sleeptime}\n')
        producer_log.write(f'Producer Chunk Size: {chunksize}\n')
        producer_log.write(f'Total {row_count} rows produced\n')
        producer_log.write(f'Execution time: {elapsed_time/60:.2f} minutes\n')
        producer_log.write(f'Rows per second: {row_count/elapsed_time:.2f}\n')