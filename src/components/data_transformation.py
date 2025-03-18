'''
Performs data preprocessing and transformation
'''
import pandas as pd
import numpy as np
from src.logger.logger import logging
from src.exception.exception import CustomException
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from src.utils.utils import save_object
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder

@dataclass
class DataTransformationConfig:
    # Path to save the preprocessor object
    preprocessor_obj_file_path: str = os.path.join("artifacts", "preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def initiate_data_transformation(self):
        try:
            pass
        except Exception as e:
            logging.info(f"Error in data ingestion: {e}")
            raise CustomException(error_message=e, error_details=sys)
        
    def initialize_data_transformation(self, train_path, test_path):
        logging.info("Initiating data transformation")
        try:
            # Load the data
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)
            logging.info("Data loaded successfully")

            preprocessing_obj = self.get_data_transformation()
            target = 'price'
            drop_columns = [target, 'id']
            X_train = train_data.drop(columns=drop_columns, axis=1)
            y_train = train_data[target]
            X_test = test_data.drop(columns=drop_columns, axis=1)
            y_test = test_data[target]

            X_train = preprocessing_obj.fit_transform(X_train)
            X_test = preprocessing_obj.transform(X_test)
            logging.info("Data transformation successful")

            # Vertical Concatenation of data
            train_arr = np.c_[X_train, y_train]
            test_arr = np.c_[X_test, y_test]

            # Save the preprocessor object
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
                )
            logging.info(f"Preprocessor object saved at: {self.data_transformation_config.preprocessor_obj_file_path}")
            return train_arr, test_arr
        
        except Exception as e:
            logging.info(f"Error in data transformation: {e}")
            raise CustomException(error_message=e, error_details=sys)
        
    
    def get_data_transformation(self):
        try:
            logging.info("Initiating data transformation")
            # Define numerical and categorical columns
            categorical_columns = ['cut', 'color', 'clarity']
            numerical_columns = ['carat', 'depth', 'table', 'x', 'y', 'z']
            
            # Define the rankings
            # Categorical sequences
            cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
            color_categories = ["D", "E", "F", "G", "H", "I", "J"]
            clarity_categories = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]

            logging.info("Pipeline Initiated")
            # Create the pipeline
            # Numerical Pipeline
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('std_scaler', StandardScaler())
                ]
            )
            # Categorical Pipeline
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('ordinal_encoder', OrdinalEncoder(categories=[cut_categories, color_categories, clarity_categories]))
                ]
            )
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', num_pipeline, numerical_columns),
                    ('cat', cat_pipeline, categorical_columns)
                ]
            )
            return preprocessor
        except Exception as e:
            logging.info(f"Error in data transformation: {e}")
            raise CustomException(error_message=e, error_details=sys)