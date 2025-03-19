import pandas as pd
import numpy as np
from src.logger.logger import logging
from src.exception.exception import CustomException
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import pickle
from src.utils.utils import load_object

@dataclass
class ModelEvaluationConfig:
    pass


class ModelEvaluation:
    def __init__(self):
        logging.info("Model Evaluation initiated")

    def initiate_model_evaluation(self, train_array, test_array):
        try:
            X_test, y_test = test_array[:,:-1], test_array[:,-1]
            # Load the model
            model_path = os.path.join("artifacts", "trained_model.pkl")
            model = load_object(file_path=model_path)
                                
            # Register the model in cloud
            # mlflow.set_registry_uri(file_path="")
            logging.info("Model Started successfully")
            
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            # Start MLFlow run
            with mlflow.start_run():
                logging.info("MLFlow run started")
                prediction = model.predict(X_test)

                rmse, mae, r2 = self.eval_metrics(y_test, prediction)

                # Run on cloud system
                if tracking_url_type_store != "file":
                    mlflow.sklearn.log_model(model, "model", registered_model_name="ml_model")
                else:
                    # Run on local system
                    mlflow.sklearn.log_model(model, "model")
            mlflow.end_run()           
        except Exception as e:
            logging.info(f"Error in data ingestion: {e}")
            raise CustomException(error_message=e, error_details=sys)
        
    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        logging.info("Evaluation metrics calculated")
        return rmse, mae, r2