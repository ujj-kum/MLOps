import pandas as pd
import numpy as np
from src.logger.logger import logging
from src.exception.exception import CustomException
import os
import sys
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    # Paths for saving raw, train and test data
    raw_data_path: str = os.path.join("artifacts", "raw_data.csv")
    train_data_path: str = os.path.join("artifacts", "train_data.csv")
    test_data_path: str = os.path.join("artifacts", "test_data.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Initiating data ingestion")
        try:
            data = pd.read_csv("playground-series-s3e8/train.csv")
            logging.info("Data ingestion successful")
            # Create the folder to save dataframe
            os.makedirs(os.path.dirname(os.path.join(self.ingestion_config.raw_data_path)),exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info(f"Data saved at: {self.ingestion_config.raw_data_path}")

            # Split the data into train and test
            logging.info("Splitting data into train and test")
            train_data, test_data = train_test_split(data, test_size=0.25, random_state=42)
            logging.info("Data split successful")

            # Save the train and test data
            os.makedirs(os.path.dirname(os.path.join(self.ingestion_config.train_data_path)),exist_ok=True)
            os.makedirs(os.path.dirname(os.path.join(self.ingestion_config.test_data_path)),exist_ok=True)
            train_data.to_csv(self.ingestion_config.train_data_path, index=False)
            test_data.to_csv(self.ingestion_config.test_data_path, index=False)
            logging.info(f"Train data saved at: {self.ingestion_config.train_data_path}")
            logging.info(f"Test data saved at: {self.ingestion_config.test_data_path}")
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            logging.info(f"Error in data ingestion: {e}")
            raise CustomException(error_message=e, error_details=sys)
        

if __name__ == "__main__":
    data_ingestion = DataIngestion()
    data_ingestion.initiate_data_ingestion()