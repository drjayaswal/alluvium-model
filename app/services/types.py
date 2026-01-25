from typing import List
from pydantic import BaseModel

class FileData(BaseModel):
    filename: str
    words: List[str]
    description: str
