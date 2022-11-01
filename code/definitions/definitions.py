from pydantic import BaseModel
from typing import List, Dict, Union, Literal


class cdfCheckPhases(BaseModel):
    install: List[str]
    pre_build: List[str]
    post_build: List[str]


class cdfBuildSpecPhases(BaseModel):
    install: List[str]
    pre_build: List[str]
    build: List[str]
    post_build: List[str]
    
class cdfDeployment(BaseModel):
    project_name: str
    security_checks: Union[Literal["true"], Literal["false"]]
    build_spec_phases: cdfBuildSpecPhases

class cdfDefinitions(BaseModel):
    checks: Dict[str, cdfCheckPhases]
    deployment: Dict[str, List[cdfDeployment]]

def parse_cdfDefinitions(json_config: dict) -> cdfDefinitions:
    definitions: cdfDefinitions = cdfDefinitions.parse_obj(json_config)
    return definitions