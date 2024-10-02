import requests
import json
import logging
import quixstreams as qs

class KafkaProducer(object):
    def __init__(self, url: str, server: str, port: str, topic: str, key: str):
        self.url = url
        self.server = server
        self.port = port
        self.app = qs.Application(broker_address=f"{self.server}:{self.port}", loglevel="DEBUG")
        self.topic = topic
        self.key = key
        
    
    def update_url(self, new_url: str):
        self.url = new_url
    
    def update_key(self, new_key: str):
        self.key = new_key

    def get_api_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch data from API: {e}")
            return None
    
    def create_topic(self):
        try:
            self.app.topic(self.topic, value_deserializer="json")
        except:
            print("error creating a topic")
    
    def produce_to_kafka(self):
        self.create_topic()
        data = self.get_api_data()
        if not data:
            logging.error("No data fetched to produce to Kafka.")
            return
        with self.app.get_producer() as producer:
            json_data = json.dumps(data)
            producer.produce(topic=self.topic, key=self.key, value=json_data)
            logging.info(f"Produced data to topic {self.topic} with key {self.key}.")
