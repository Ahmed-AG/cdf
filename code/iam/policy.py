from pydantic import BaseModel
from typing import List, Union, Literal


class cdfIamStatement(BaseModel):
    Action: str
    Resource: str
    Effect: Union[Literal["Allow"], Literal["Deny"]]

class cdfIamPolicy(BaseModel):
    Statement: List[cdfIamStatement]

def make_iam_policy(json_config: dict) -> cdfIamPolicy:
    policy: cdfIamPolicy = cdfIamPolicy.parse_obj(json_config)
    return policy