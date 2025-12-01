"""
Load and preprocess data.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# import plotly.express as px
import pickle
import os
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression  
from sklearn.metrics import accuracy_score

_preprocessor = None

def load_data(path: str) -> pd.DataFrame:
    """Load data from seaborn data,
    put it in cache and return a DataFrame."""
    pingouins = sns.load_dataset("penguins")
   
    if not os.path.exists("data"):
        os.makedirs("data")
        
    # Drop the island column becuase it's exactly the target variable in disguise
    pingouins.drop(columns=["island"], inplace=True)
    pingouins.to_csv(path, index=False)
    
    # Save in cache 
    with open(path, "wb") as f:
        pickle.dump(pingouins, f)
    
    #Handle potential errors (file not found, etc.)

    return pingouins

def get_X_y(
    df: pd.DataFrame, target_column: str, target:bool = True
) -> tuple[pd.DataFrame, pd.Series]:
    """Split DataFrame into features and target."""
    
    if (target):
        y = df.pop(target_column)
        X = df
    else :
        y = None
        X = df
    return ([X, y])

def split_data(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split data into training and testing sets."""
    
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, random_state=random_state, stratify=y
    ) 

    return ([X_train, X_test, y_train, y_test])

def preprocess_data(X: pd.DataFrame
                    ,fit = True) -> pd.DataFrame:
    global _preprocessor
    """Preprocess data: handle missing values, encode categorical variables, scale numerical features."""
    
    num_pipe = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    cat_pipe = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),   
        ('encoder', OneHotEncoder(sparse_output=False, drop="first"))
    ])
    
    if fit:
        # Create and fit preprocessor
        _preprocessor = ColumnTransformer(transformers=[
            ('num', num_pipe, make_column_selector(dtype_include="number")),
            ('cat', cat_pipe, make_column_selector(dtype_include=object))
        ])
        _preprocessor.set_output(transform="pandas")
        # print(_preprocessor)
        _preprocessor.fit(X)
        
    # preprocessor = ColumnTransformer(transformers=[
    #     ('num', num_pipe, make_column_selector(dtype_include="number")),
    #     ('cat', cat_pipe, make_column_selector(dtype_include=object))
    # ])
    
    # preprocessor.fit(X)
    # X_train_preproc = _preprocessor.transform(X)
    # X_test_preproc = preprocessor.transform(X)
    
    
    return pd.DataFrame(_preprocessor.transform(X))

def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> LogisticRegression    :
    logi = LogisticRegression()
    # print(type(logi))
    # print(logi.fit(X_train,y_train))
    model = logi.fit(X_train,y_train)
    return model

def evaluate_model(model: LogisticRegression , X_test: pd.DataFrame, y_test: pd.Series) -> float:
    print(X_test)
    print(y_test)
    print(model)
    y_pred = model.predict(X_test)
    print(y_pred)
    score = accuracy_score(y_test,y_pred)
    print( score)
    return 0
    