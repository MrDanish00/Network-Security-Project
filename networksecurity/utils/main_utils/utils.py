import dill
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import numpy as np
import os, sys
import yaml
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path,"rb") as file_obj:
            return yaml.safe_load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def write_yaml_file(file_path:str, content:object, replace:bool = True) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)

    except Exception as e:
        raise NetworkSecurityException(e,sys)

def save_numpy_arr(file_path:str, arr:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file:
            np.save(file, arr)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def load_numpy_arr(file_path:str,) -> np.array:
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_path)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def save_object(file_path:str, obj:object):
    try:
        logging.info("Entered save_object function of main_utils class")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file:
            pickle.dump(obj, file)
        logging.info("Exited save_object function of main_utils class")
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def load_object(file_path:str,) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file {file_path} is not exists.")
        with open(file_path,"rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def evaluate_models(X_train,y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train,y_train_pred)
            test_model_score = r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]] = test_model_score
            
        return report
    except Exception as e:
        raise NetworkSecurityException(e,sys)