from pydantic import BaseModel
from typing import List


class cdfIamStatement(BaseModel):
    Action: str
    Resource: str
    Effect: str

class cdfIamPolicy(BaseModel):
    Statement: List[cdfIamStatement]
