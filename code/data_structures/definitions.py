from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum
from typing import List, Dict
import json


class cdfDeploymentTypes(Enum):
    CFN = "cfn"
    TERRAFORM = "terraform"

class cdfCheckTypes(Enum):
    GENERAL_ALL = "general_all"
    CFN_NAG = "cfn_nag"
    CHECKOV = "checkov"
    SNYK = "snyk"

@dataclass_json
@dataclass
class cdfCheckPhases:
    install: List[str]
    pre_build: List[str]
    post_build: List[str]

@dataclass_json
@dataclass
class cdfBuildSpecPhases:
    install: List[str]
    pre_build: List[str]
    build: List[str]
    post_build: List[str]
    
@dataclass_json
@dataclass
class cdfDeployment:
    project_name: str
    security_checks: str
    build_spec_phases: cdfBuildSpecPhases

@dataclass_json
@dataclass
class cdfDefinitions:
    checks: Dict[cdfCheckTypes, cdfCheckPhases]
    deployment: Dict[cdfDeploymentTypes, List[cdfDeployment]]


def validate_definitions(definitions: Dict) -> Dict:
    schema_validate = cdfDefinitions.schema().validate(definitions)

    if schema_validate:
        return {
            "error" : schema_validate
        }
    else:
        return {}
if __name__ == "__main__":
    with open("config.d/definitions.json", "r") as f:
        raw_object = json.load(f)
    # print(raw_object)
    definitions = cdfDefinitions.from_json(json.dumps(raw_object))
    print(definitions)