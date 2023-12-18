import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging





from src.utils import save_object,evaluate_models

@dataclass
class ModelTrainingConfig:
    trained_model_fit_path=os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainingConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("splitting training and test input data")
            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],  # Fix the indexing here
                test_array[:, :-1],
                test_array[:, -1],  # Fix the indexing here
            )
            models = {
                "random forest": RandomForestRegressor(),
                "DecisionTree": DecisionTreeRegressor(),
                "Gradient boosting": GradientBoostingRegressor(),
                "LinearRegression": LinearRegression(),
                "KNeighbors classifier": KNeighborsRegressor(),
                "XGBRegressor": XGBRegressor(),
                "CatBoostRegressor": CatBoostRegressor(),
                "AdaBoostRegressor": AdaBoostRegressor()
            }

            model_report: dict = evaluate_models(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test,
                                                 models=models)

            # Get the best model score from the dict
            best_model_score = max(sorted(model_report.values()))

            # Get the best model name from the dict
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found")

            logging.info("Best found model on both training and testing data")

            save_object(
                file_path=self.model_trainer_config.trained_model_fit_path,
                obj=best_model
            )

            predicted = best_model.predict(x_test)

            r2_score_value = r2_score(y_test, predicted)
            return r2_score_value

        except Exception as e:
            raise CustomException(e, sys)






