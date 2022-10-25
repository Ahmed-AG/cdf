from pydantic import BaseModel
from typing import List, Dict


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
    security_checks: str
    build_spec_phases: cdfBuildSpecPhases

class cdfDefinitions(BaseModel):
    checks: Dict[str, cdfCheckPhases]
    deployment: Dict[str, List[cdfDeployment]]