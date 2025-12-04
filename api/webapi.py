import pandas as pd
from fastapi import FastAPI
import loguru

from api.data_models  import Pengouin
from pengouins.data import preprocess_data
from pengouins.registry import load_model

app = FastAPI()
logger = loguru.logger

@app.get("/")
async def read_root():
    return {"message": "🐧" }

@app.post("/predict") 
async def predict(pengouin: Pengouin) -> dict:
    """
    Make a prediction for one row 
    """
    # Reformat input data
    logger.debug(f"{pengouin=}")
    logger.debug(f"{pengouin.model_dump()=}")
    data = pd.DataFrame([pengouin.model_dump()])
    # Preprocess data
    preprocessor = load_model("models/preprocessor.pkl")
    _ , data_preproc = preprocess_data(data, preprocessor)
    # Load model and make prediction
    model = load_model("models/pengouin_classifier.pkl")
    logger.debug(f"{data_preproc=}")
    prediction = model.predict(data_preproc)
    logger.debug(f"{prediction=}")
    # Return prediction as a fastapi friendly format
    return {"species": prediction[0]}

from fastapi import UploadFile

@app.post("/predict_batch")
async def predict_batch(pengouins: UploadFile) -> dict:
    """
    Make predictions for a batch of rows 
    """
    # Read uploaded file
    df = pd.read_csv(pengouins.file)
    logger.debug(f"{df=}")
    # Preprocess data
    preprocessor = load_model("models/preprocessor.pkl")
    _ , data_preproc = preprocess_data(df, preprocessor)
    # Load model and make prediction
    model = load_model("models/pengouin_classifier.pkl")
    logger.debug(f"{data_preproc=}")
    predictions = model.predict(data_preproc)
    logger.debug(f"{predictions=}")
    # Return prediction as a fastapi friendly format
    return {"species": predictions.tolist()}