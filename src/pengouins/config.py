
import os
from pathlib import Path


class Config:
    """Configuration class for managing environment variables."""
    
    # Storage configuration
    MODEL_STORAGE_MODE = os.getenv("MODEL_STORAGE_MODE", "local")
    # MLflow configuration
    MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "mlruns")
    MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "penguin_classification")
    MODEL_NAME = os.getenv("MODEL_NAME", "penguin_classifier")
    
    # Local storage configuration
    LOCAL_MODEL_DIR = os.getenv("LOCAL_MODEL_DIR", "models")
    
    @classmethod
    def use_mlflow(cls) -> bool:
        """Check if MLflow tracking is enabled."""
        return cls.MODEL_STORAGE_MODE.lower() == "mlflow"
    
    @classmethod
    def get_model_path(cls, model_name: str) -> Path:
        """Get the path for saving/loading models."""
        return Path(cls.LOCAL_MODEL_DIR) / f"{model_name}.pkl"
    
    @classmethod
    def display_config(cls):
        """Display current configuration."""
        print("=" * 50)
        print("📊 MLFLOW CONFIGURATION")
        print("=" * 50)
        print(f"Storage Mode: {cls.MODEL_STORAGE_MODE}")
        print(f"Use MLflow: {cls.use_mlflow()}")
        if cls.use_mlflow():
            print(f"MLflow Tracking URI: {cls.MLFLOW_TRACKING_URI}")
            print(f"Experiment Name: {cls.MLFLOW_EXPERIMENT_NAME}")
            print(f"Model Name: {cls.MODEL_NAME}")
        else:
            print(f"Local Model Directory: {cls.LOCAL_MODEL_DIR}")
        print("=" * 50)


# Display configuration on import (optional, for debugging)
if __name__ == "__main__":
    Config.display_config()