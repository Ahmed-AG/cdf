from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List, Dict

@dataclass_json
@dataclass
class cdfIamStatement:
    Action: str
    Resource: str
    Effect: str

@dataclass_json
@dataclass
class cdfIamPolicy:
    Statement: List[cdfIamStatement]

def validate_iam_policy(policy: Dict) -> Dict:
    schema_validate = cdfIamPolicy.schema().validate(policy)
    if schema_validate:
        return {
            "error" : schema_validate
        }
    else:
        return {}