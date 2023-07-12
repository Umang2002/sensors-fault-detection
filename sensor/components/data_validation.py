from sensor.constant.training_pipeline import SCHEMA_FILE_PATH

from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artifact_entity import DataValidationArtifact,DataIngestionArtifact
from sensor.utills.main_utills import read_yaml_file

from sensor.exception import SensorException
from sensor.logger import logging
import pandas as pd
import os,sys



class DataValidation:


    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e,sys)

    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self._schema_config['columns'])

            if len(dataframe.columns)==number_of_columns:
                return True
            return False
            
        
        except Exception as e:
            raise SensorException(e,sys)

    def is_numerical_column_exists(self,dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns=len(self._schema_config['numerical_columns'])
            dataframe_columns = dataframe.columns

            numerical_columns_present=True
            missing_numerical_columns = []
            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_columns_present=False
                    missing_numerical_columns.append(num_column)
            logging.info(f"Number of Missing numerical columsn is {len(missing_numerical_columns)}")
            return numerical_columns_present
            
        except Exception as e:
            raise SensorException(e,sys)
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e,sys)

    def detect_dataset_drift(self):
        pass

    def initiate_data_validation(self)->DataIngestionArtifact:
        try:
            error_message=""
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_fil_path = self.data_ingestion_artifact.test_file_path
            
            # This is for the read_data part
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_fil_path)
            
            # now the validate number of columns part
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message=f"{error_message} Train dataframe has not same number of columns"

            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message=f"{error_message} Test dataframe has not same number of columns"   
            
            # Validate number of numerical columns
            status = self.is_numerical_column_exists(dataframe=train_dataframe)
            if not status:
                error_message=f"{error_message} Train dataframe does not contain all numerical columns"

            status = self.is_numerical_column_exists(dataframe=test_dataframe)
            if not status:
                error_message=f"{error_message} Test dataframe does not contain all numerical columns"
          
            if len(error_message) > 0:
                raise Exception(error_message)
            
            # let check the data drift score 
        
        except Exception as e:
            raise SensorException(e,sys)
