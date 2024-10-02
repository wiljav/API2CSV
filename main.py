import logging
import os
# import subprocess
from dotenv import load_dotenv
from real_time_data_simulator import RealTimeData
from blob_minio import MinioBlob
from data_validator import validate_data
from pydantic import ValidationError
import pandas as pd

# Load environment variables from .env file
load_dotenv("credentials.env")

# Retrieve username and password
ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

def save_locally(file_name: str, local_path: str, data: str, delimiter: str = ";"):
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(os.path.join(local_path, file_name), index=False, sep=delimiter)
    print(f"File {file_name} saved to the directory {local_path}")
    

def main():
    print(f"ACCESS_KEY: {ACCESS_KEY}")
    print(f"SECRET_KEY: {SECRET_KEY}")
    server = "localhost"
    port = "29092"
    topic = "drinks_data_combined"
    key = f"drinks_recipes"
    url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?f="
    chars = "a"#bcdefghijklmnopqrstuvwxyz0123456789"
    chars = list(chars)
    minio_bucket = "minio-bucket"
    minio_blob = MinioBlob(client=server,
                           port="9000",
                           access_key=ACCESS_KEY,
                           secret_key=SECRET_KEY)
    fetched_data = RealTimeData(server=server, port=port, url=url, chars=chars, topic=topic, key=key, interval=5)
    final_data = fetched_data.run()
    print("validating data ...")
    dt = final_data[0]['drinks']
    try:
        _, invalid_count = validate_data(dt)
    except ValidationError as e:
        print(f"Validation error: {e}")
    except TypeError as e:
        print("Type error:", e)
    except ValueError as e:
        print("Value error:", e)
    print(f"Data is Validated")
    
    print("Saving to Minio...")
    if final_data and invalid_count == 0:
        logging.info("Saving data to MinIO")
        file_name = "drinks.csv"
        minio_blob.save_to_minio(minio_bucket, file_name, data=final_data)
        print(f"Data saved to Minio, within '{minio_bucket}/{file_name}'")

        print("Saving data locally...")
        save_locally(file_name="drinks.csv", local_path="./app/minio_data", data=dt, delimiter=";")

    elif invalid_count != 0:
        print("Data is invalid")
    else:
        logging.error("No data collected from the simulation.")

if __name__ == '__main__':
    main()
    
