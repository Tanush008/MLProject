import sys
import os
import pandas as pd
import numpy as np
from src.logger import logging
from src.expection import CustomException
from dataclasses import dataclass
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from src.utils import save_obj


@dataclass
class DataTransConfig:
    preprocess_obj_file_path = os.path.join('artifacts', "preproccesor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_trans_config = DataTransConfig()

    def get_data_trans_obj(self):
        # this func is res for
        try:
            numerical_col = ['reading_score', 'writing_score']
            categorical_col = ["gender",
                               "race_ethnicity",
                               "parental_level_of_education",
                               "lunch",
                               "test_preparation_course",]
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encode", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"Categorical columns: {categorical_col}")
            logging.info(f"Numerical columns: {numerical_col}")

            preprocessor = ColumnTransformer(
                [
                    ("num_piplines", num_pipeline, numerical_col),
                    ("cat_pipelines", cat_pipeline, categorical_col)
                ]
            )
            return preprocessor
        except CustomException as e:
            raise CustomException(e, sys)
        
        
    def intiate_data_transformer(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preproccesor_obj = self.get_data_trans_obj()

            target_col_name = 'math_score'
            numerical_col = ['writing_score', 'reading_score']
            input_feature_train = train_df.drop(
                columns=[target_col_name], axis=1)
            target_feature_train = train_df[target_col_name]

            input_feature_test = test_df.drop(
                columns=[target_col_name], axis=1)
            target_feature_test = test_df[target_col_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_test_arr = preproccesor_obj.fit_transform(
                input_feature_test)

            input_feature_train_arr = preproccesor_obj.fit_transform(
                input_feature_train)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test)
            ]
            logging.info(f"Saved preprocessing object.")

            save_obj(

                file_path=self.data_trans_config.preprocess_obj_file_path,
                obj=preproccesor_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_trans_config.preprocess_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)
