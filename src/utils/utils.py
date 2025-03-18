'''
Contains utility functions for the project
'''
import os
import sys
import pickle
import numpy as np
import pandas as pd
from src.logger.logger import logging
from src.exception.exception import CustomException
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def save_object(file_path, obj):
    '''
    Save the object(models/preprocessing objects) to the file path
    '''
    try:
        dir_path = os.path.dirname(p=file_path)
        os.makedirs(name=dir_path, exist_ok=True)
        with open(file_path, 'wb') as file:
            pickle.dump(obj=obj, file=file)
    except Exception as e:
        raise CustomException(error_message=e, error_details=sys)
    

def load_object(file_path):
    '''
    Load the object(models/preprocessing objects) from the file path
    '''
    try:
        with open(file_path, 'rb') as file:
            obj = pickle.load(file=file)
        return obj
    except Exception as e:
        logging.info(f"Error in loading object: {e}")
        raise CustomException(error_message=e, error_details=sys)
    
    
def evaluate_model(X_train, y_train, X_test, y_test, models):
    '''
    Evaluate the model using the test data
    '''
    try:
        report = {}
        for i in range(len(models)):
            model = list(models.values())[i]
            # Train Model
            model.fit(X_train, y_train)

            # Predict Testing data
            y_pred_test = model.predict(X_test)

            # Get R2 scores for train and test
            test_model_score = r2_score(y_test, y_pred_test)

            report[list(models.keys())[i]] =  test_model_score
        return report
    except Exception as e:
        logging.info(f"Error in evaluating model: {e}")
        raise CustomException(error_message=e, error_details=sys)
