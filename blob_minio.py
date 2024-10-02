from minio import Minio
from io import BytesIO, StringIO
import logging
import json
import pandas as pd

class MinioBlob(object):
    def __init__(self, client: str, port: str, access_key: str, secret_key: str, secure=False):
        self.client = client
        self.port = port
        self.access_key = access_key
        self.secret_key = secret_key
        self.secure = secure
        self.minio_client = Minio(f"{self.client}:{self.port}",
                                  access_key=self.access_key,
                                  secret_key=self.secret_key,
                                  secure=self.secure)

    def save_to_minio(self, bucket_name: str, file_name: str, data, as_csv=True):
        self.bucket_name = bucket_name
        self.file_name = file_name
        self.data = data

        if as_csv:
            self.length = len(self.data)
            self.dataframe = pd.DataFrame()
            for i in range(self.length):
                self.dataframe = pd.concat([self.dataframe, pd.DataFrame(self.data[i])], ignore_index=True)
            self.csv_buffer = StringIO()
            self.dataframe.to_csv(self.csv_buffer, index=False)
            self.data_bytes = self.csv_buffer.getvalue().encode('utf-8')
        else:
            # Converting JSON data to bytes
            self.data_bytes = json.dumps(self.data).encode('utf-8')

        # Checking if bucket exists
        if not self.minio_client.bucket_exists(self.bucket_name):
            self.minio_client.make_bucket(self.bucket_name)
            logging.info(f"Created bucket: {self.bucket_name}")

        self.minio_client.put_object(
            bucket_name=self.bucket_name,
            object_name=self.file_name,
            data=BytesIO(self.data_bytes),
            length=len(self.data_bytes),
            content_type="application/csv"
        )
        logging.info(f"Saved file to MinIO: {self.file_name}")
