import json
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List, Dict

@dataclass_json
@dataclass
class Source:
    source_type: str
    repo_name: str
    branch: str

@dataclass_json
@dataclass
class Assume_role:
    role: str

@dataclass_json
@dataclass
class Deployment:
    assume_role: Assume_role
    aws_account: str
    region: str
    type: str
    parameters: str
    capabilities: str
    deployment_file: str
    iam_policy_file: str
    checks: List[str]

@dataclass_json
@dataclass
class Pipeline:
    name: str
    provider: str
    source: Source
    deployment: Deployment
    

@dataclass_json
@dataclass
class Statement:
    Action: str
    Resource: str
    Effect: str

@dataclass_json
@dataclass
class Iam_policy:
    Statement: List[Statement]

def validate_pipeline_config(pipeline: Dict) -> Dict:
    schema_validate = Pipeline.schema().validate(pipeline)

    if schema_validate:
        return {
            "pipeline_name": pipeline['name'],
            "error" : schema_validate
        }
    else:
        return {}

def validate_iam_policy(policy: Dict) -> Dict:
    schema_validate = Iam_policy.schema().validate(policy)
    if schema_validate:
        return {
            "error" : schema_validate
        }
    else:
        return {}