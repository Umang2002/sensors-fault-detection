from sensor.configuration.mongo_db_connection import MongoDBClient
import os,sys

from sensor.logger import logging
from sensor.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.exception import SensorException



if __name__ =="__main__":
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
    except Exception as e:
        logging.exception(e)
        