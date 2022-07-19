from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List, Dict

@dataclass_json
@dataclass
class Source_Config:
    source_type: str
    repo_name: str
    branch: str

@dataclass_json
@dataclass
class Assume_role:
    role: str

@dataclass_json
@dataclass
class Deployment_Config:
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
    source: Source_Config
    deployment: Deployment_Config
    

def validate_pipeline_config(pipeline: Dict) -> Dict:
    schema_validate = Pipeline.schema().validate(pipeline)

    if schema_validate:
        return {
            "pipeline_name": pipeline['name'],
            "error" : schema_validate
        }
    else:
        return {}

