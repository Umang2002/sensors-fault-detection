import os,sys
import pandas as pd
import numpy as np
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from sensor.entity.config_entity import DataTransformationConfig
from sensor.ml.model.estimator import TargetValueMapping
from sensor.utills.main_utills import save_numpy_array_data,save_object

class DataTransformation:

    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise SensorException(e,sys)
        
    

    @staticmethod
    def read_data(file_path)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e,sys)
        
    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            robust_scaler = RobustScaler()
            simple_imputer = SimpleImputer(strategy="constant", fill_value=0)
            preprocessor = Pipeline(
                steps=[
                    ("Imputer",simple_imputer),
                    ("RobustScaler",robust_scaler)
                ]
            )

            return preprocessor
        except Exception as e:
            raise SensorException(e,sys)


 
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            # call the data_transformation_object function()
            preprocessor = self.get_data_transformer_object()

            # split the train and test datasets
            # train dataset splitting
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(TargetValueMapping().to_dict())

            #splitting the test data into target and train
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping().to_dict())

            # applying the preprocessor object
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transform_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transform_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            #smt
            smt = SMOTETomek(sampling_strategy="minority")


            # fit and transform on both train and test smt
            input_feature_train_final, target_feature_train_final = smt.fit_resample(transform_input_train_feature,target_feature_train_df)
            input_feature_test_final,target_feature_test_final = smt.fit_resample(transform_input_test_feature,target_feature_test_df)
 
            # concatinate the train and target column
            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]

            # save array into train and test npy files
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array = train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array = test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object)

            
            # for the creating artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path 
            )

            logging.info(f"Data Transformation artifact craeted at:{data_transformation_artifact}")
            return data_transformation_artifact
        
        except Exception as e:
            raise SensorException(e,sys)
