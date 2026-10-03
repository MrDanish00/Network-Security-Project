from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import pandas as pd
import os, sys
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constant.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import save_numpy_arr, save_object


class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact = data_validation_artifact
            self.data_transformation_config:DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def get_data_transformer_obj(cls) -> Pipeline:
        logging.info("Entered get_data_transformer_obj method of DataTransformation class.")
        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialize parameters are: {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor:Pipeline = Pipeline([("imputer",imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_file(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation method")
        try:
            logging.info("Starting data transformation")
            train_df = DataTransformation.read_file(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_file(self.data_validation_artifact.valid_test_file_path)

            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            preprocessor = self.get_data_transformer_obj()
            preprocessor_obj = preprocessor.fit(input_feature_train_df)
            transformed_input_feature_train = preprocessor_obj.transform(input_feature_train_df)
            transformed_input_feature_test = preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_feature_train,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_feature_test, np.array(target_feature_test_df)]

            save_numpy_arr(self.data_transformation_config.transformed_train_file_path, arr=train_arr)
            save_numpy_arr(self.data_transformation_config.transformed_test_file_path, arr=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_obj)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)