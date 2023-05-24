from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    image: str = ''
    email:str =''
    password: str  =''
    status: int = 0
    role: int = 1
    accessed_at = []
    code:str=''
    code_created_at:datetime =datetime.now()
    created_at: datetime = datetime.now()