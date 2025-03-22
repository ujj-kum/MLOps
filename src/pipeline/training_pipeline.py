# This is the main file. This file will be used to run the entire pipeline.
# Every component of the pipeline will be called from this file.

import os
import sys
from src.logger.logger import logging
from src.exception.exception import CustomException
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation

import pandas as pd

obj = DataIngestion()
train_path, test_path = obj.initiate_data_ingestion()

data_transformation = DataTransformation()
train_array, test_array = data_transformation.initialize_data_transformation(train_path, test_path)

model_trainer = ModelTrainer()
model_trainer.initiate_model_training(train_array, test_array)

# Evaluate the model
model_evaluation = ModelEvaluation()
model_evaluation.initiate_model_evaluation(train_array, test_array)

# Encapsulating everything in a class
class TrainingPipeline:
    def start_data_ingestion(self):
        try:
            data_ingestion = DataIngestion()
            train_path, test_path = data_ingestion.initiate_data_ingestion()
            return train_path, test_path
        except CustomException as e:
            raise CustomException(e, sys)
        
    def start_data_transformation(self, train_path, test_path):
        try:
            data_transformation = DataTransformation()
            train_array, test_array = data_transformation.initialize_data_transformation(train_path, test_path)
            return train_array, test_array
        except CustomException as e:
            raise CustomException(e, sys)
        
    def start_model_training(self, train_array, test_array):
        try:
            model_trainer = ModelTrainer()
            model_trainer.initiate_model_training(train_array, test_array)
        except CustomException as e:
            raise CustomException(e, sys)
        
    def start_training(self):
        try:
            train_path, test_path = self.start_data_ingestion()
            train_array, test_array = self.start_data_transformation(train_path, test_path)
            self.start_model_training(train_array, test_array)
        except CustomException as e:
            raise CustomException(e, sys)