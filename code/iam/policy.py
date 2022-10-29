from pydantic import BaseModel
from typing import List


class cdfIamStatement(BaseModel):
    Action: str
    Resource: str
    Effect: str

class cdfIamPolicy(BaseModel):
    Statement: List[cdfIamStatement]

def make_iam_policy(json_config: dict) -> cdfIamPolicy:
    policy: cdfIamPolicy = cdfIamPolicy.parse_obj(json_config)
    return policy