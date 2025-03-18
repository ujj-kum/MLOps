import pandas as pd
import numpy as np
from src.logger.logger import logging
from src.exception.exception import CustomException
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from src.utils.utils import save_object, evaluate_model
from sklearn.linear_model import LogisticRegression, Ridge, Lasso

@dataclass
class ModelTrainerConfig:
    # Save the trained model pkl file here
    trained_model_file_path = os.path.join("artifacts", "trained_model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        
        

    def initiate_model_training(self, train_array, test_array):
        try:
            logging.info("Splitting data into train and test")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )
            # Definig the models
            models = {
            'LinearRegression': LogisticRegression(),
            'Lasso': Lasso(),
            'Ridge': Ridge(),
            }
            model_report:dict = evaluate_model(X_train, y_train, X_test, y_test, models)
            print(model_report)
            print("\n==============================\n")
            logging.info(f"Model Report: {model_report}")

            # Get the best model
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]
            print(f"Best Model: {best_model_name} with R2 Score: {best_model_score}")
            print("\n==============================\n")
            logging.info(f"Best Model: {best_model_name} with R2 Score: {best_model_score}")
            # Save the best model
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=best_model)
        except Exception as e:
            logging.info(f"Error in data ingestion: {e}")
            raise CustomException(error_message=e, error_details=sys)