from dataclasses import dataclass
from dataclasses_json import dataclass_json
import definitions
from typing import List, Dict
from enum import Enum
import json


class cdfDeploymentTypes(Enum):
    CFN = "cfn"
    TERRAFORM = "terraform"


@dataclass_json
@dataclass
class cdfSource:
    source_type: str
    repo_name: str
    branch: str

@dataclass_json
@dataclass
class Assume_role:
    role: str

@dataclass_json
@dataclass
class cdfDeploymentcfn:
    assume_role: Assume_role
    aws_account: str
    region: str
    type: cdfDeploymentTypes
    parameters: str
    capabilities: str
    deployment_file: str
    iam_policy_file: str
    checks: List[definitions.cdfCheckTypes]

@dataclass_json
@dataclass
class cdfDeploymentTerraform:
    assume_role: Assume_role
    aws_account: str
    region: str
    type: cdfDeploymentTypes
    parameters: str
    deployment_folder: str
    iam_policy_file: str
    checks: List[definitions.cdfCheckTypes]


@dataclass_json
@dataclass
class cdfPipeline:
    name: str
    provider: str
    source: cdfSource
    deployment: cdfDeploymentcfn | cdfDeploymentTerraform
    

def validate_pipeline_config(pipeline: Dict) -> Dict:
    schema_validate = cdfPipeline.schema().validate(pipeline)

    if schema_validate:
        return {
            "pipeline_name": pipeline['name'],
            "error" : schema_validate
        }
    else:
        return {}

if __name__ == "__main__":
    with open("config.d/config.json", "r") as f:
        raw_object = json.load(f)
    # print(raw_object)
    for pipeline in raw_object['pipelines']:
        config = cdfPipeline.from_json(json.dumps(pipeline))
        print(config)