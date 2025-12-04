from pydantic import BaseModel
from typing import Literal 

class Pengouin(BaseModel):
    bill_length_mm: float
    bill_depth_mm: float
    flipper_length_mm: float
    body_mass_g: float 
    sex: Literal["Male", "Female"] 
    
    
