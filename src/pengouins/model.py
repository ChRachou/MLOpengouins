
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import loguru
import mlflow


from pengouins.registry import save_model
from pengouins.config import Config

def train_model(  X_train : pd.DataFrame
                , y_train: pd.Series) -> LogisticRegression:
    """Train a model on the training data."""
    loguru.logger.info("Training Model...")
    # Log parameters if using MLflow
    model_params = {
               "max_iter":100
              , "solver":"liblinear"
              , "C":1.0}
    params = {  "model_type": "LogisticRegression"
              , "n_samples": len(X_train)
              , "n_features": X_train.shape[1]
              , **model_params}
    if Config.use_mlflow():
        mlflow.log_params(params)
        
    logi = LogisticRegression(**model_params)
    logi.fit(X_train, y_train)
    save_model(logi,"pengouin_classifier", X=X_train)
    return logi
    

def evaluate_model( model
                    , X_test: pd.DataFrame
                    , y_test: pd.Series) -> float:
    """Evaluate the model on the test data and return accuracy."""
    y_pred = model.predict(X_test)
    acc = round(accuracy_score(y_pred,y_test),3)
    if Config.use_mlflow():
        mlflow.log_metric("accuracy", acc)
    return acc