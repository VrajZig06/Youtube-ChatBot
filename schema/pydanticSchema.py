from pydantic import BaseModel

class APIResponse(BaseModel):
    result : str
    
class APIInput(BaseModel):
    url: str
    query : str
    