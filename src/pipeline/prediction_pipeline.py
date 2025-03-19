# Code for web application
import os
import sys
import pandas as pd
from src.exception.exception import CustomException
from src.logger.logger import logging
from src.utils.utils import load_object, evaluate_model



class PredictionPipeline:
    def __init__(self):
        pass
    
    def predict(self, features):
        try:
            # Load the preprocessed object
            preprocessed_object = load_object(file_path=os.path.join("artifacts", "preprocessor.pkl"))
            # Transform the data
            scaled_features = preprocessed_object.transform(features)
            # Load the trained model
            model = load_object(file_path=os.path.join("artifacts", "trained_model.pkl"))
            # Predict the data
            prediction = model.predict(scaled_features)
            return prediction
        except Exception as e:
            raise CustomException(error_message=e, error_details=sys)
        

class CustomData:
    def __init__(self, 
                 carat: float, 
                    depth: float, 
                    table: float, 
                    x: float, 
                    y: float, 
                    z: float, 
                    cut: str, 
                    color: str, 
                    clarity: str):
        self.carat = carat
        self.depth = depth
        self.table = table
        self.x = x
        self.y = y
        self.z = z
        self.cut = cut
        self.color = color
        self.clarity = clarity

    def get_data_as_dataframe(self):
        try:
            custom_data_dict = {
                "carat": [self.carat],
                "depth": [self.depth],
                "table": [self.table],
                "x": [self.x],
                "y": [self.y],
                "z": [self.z],
                "cut": [self.cut],
                "color": [self.color],
                "clarity": [self.clarity]
            }
            # Convert the dictionary to a dataframe
            data = pd.DataFrame(custom_data_dict)
            return data
        except Exception as e:
            raise CustomException(error_message=e, error_details=sys)
