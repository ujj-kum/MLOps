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
        pass

    def initiate_model_evaluation(self):
        try:
            pass
        except Exception as e:
            logging.info(f"Error in data ingestion: {e}")
            raise CustomException(error_message=e, error_details=sys)