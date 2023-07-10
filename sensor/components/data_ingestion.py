from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
import os,sys
from pandas import DataFrame

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SensorException(e,sys)

    def export_data_into_featutre_stor(self) -> DataFrame:
        """
        Export mongodb collection record as data frame into feature
        """
        pass

    def split_data_as_train_test(self,dataframe:DataFrame) -> None:
        """
        Feature store dataset will be divided into train and test split
        """
        
        pass

   
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
         try:
             pass
         except Exception as e:
             raise SensorException(e,sys)