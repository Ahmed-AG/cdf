from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List, Dict


@dataclass_json
@dataclass
class Check_Type:
    install: List[str]
    pre_build: List[str]
    post_build: List[str]

@dataclass_json
@dataclass
class Deployment_Type:
    install: List[str]
    pre_build: List[str]
    build: List[str]
    post_build: List[str]

@dataclass_json
@dataclass
class Definitions:
    checks: Dict[str, Check_Type]
    deployment: Dict[str, Deployment_Type]

    def get_checks(self) -> Dict[str, str]:
        return self.checks.to_json()

def validate_definitions(definitions: Dict) -> Dict:
    schema_validate = Definitions.schema().validate(definitions)

    if schema_validate:
        return {
            "error" : schema_validate
        }
    else:
        return {}
