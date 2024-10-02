import time
from kafka_producer import KafkaProducer
import logging

class RealTimeData:
    def __init__(self, url: str, server: str, port: int, topic: str, key: str, chars: list, interval: int = 600):
        self.url = url
        self.server = server
        self.port = port
        self.topic = topic
        self.key = key
        self.chars = chars
        self.interval = interval
        self.producer = KafkaProducer(url=self.url,
                                      server=self.server,
                                      port=self.port,
                                      topic=self.topic,
                                      key=self.key)
        self.data_collected = []
        
    def simulate_real_time(self):
        for char in list(self.chars):
            new_url = f"{self.url}{char}"
            new_key = f"{self.key}_{char}"
            
            self.producer.update_url(new_url)
            self.producer.update_key(new_key)
        
        # Fetching the API data and store it in the data_collected list
            data = self.producer.get_api_data()
            if data:
                self.data_collected.append(data)
                self.producer.produce_to_kafka()
                logging.info(f"Produced data for {char}")
            else:
                logging.error(f"Failed to get data for {char}")
            logging.info(f"Produced data for {char}")
            logging.info(f"Waiting {self.interval/60} minutes before fetching the next page...")
            # time.sleep(self.interval)
        return self.data_collected
    
    def run(self):
        logging.info("Starting real-time data simulation using Kafka...")
        return self.simulate_real_time()