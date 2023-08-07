from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact

# common imports
from sensor.exception import SensorException
import os,sys
from sensor.logger import logging

# components 
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer

class TrainPipeline():

    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        # self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        # self.training_pipeline_config = training_pipeline_config

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data ingestion")

            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact= data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion Completed and artifact:{data_ingestion_artifact}")
            return data_ingestion_artifact
        
        except Exception as e:
            raise SensorException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data Validation")

            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data Validation is Completed!!")
            return data_validation_artifact
        
        except Exception as e:
            raise SensorException(e,sys)  
           
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Start data transformation")
            
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data transformation Completed!!")
            return data_transformation_artifact
        
        except Exception as e:
            raise SensorException(e,sys)   
        
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Start model training")

            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,model_trainer_config=model_trainer_config)
            model_trainer_artifact = model_trainer.initiate_model_training()
            logging.info("Model Training is completed!")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e,sys)
        
    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)
        
    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)   
        
    def run_pipeline(self):
        try:
           data_ingestion_artifact:DataIngestionArtifact= self.start_data_ingestion()
           data_validation_artifact= self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
           data_transformation_artifact= self.start_data_transformation(data_validation_artifact=data_validation_artifact)   
           model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
           return model_trainer_artifact  
        
        except Exception as e:
            raise SensorException(e,sys) 


