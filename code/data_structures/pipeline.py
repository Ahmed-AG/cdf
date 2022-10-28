from typing import List, Literal, Optional
from typing import Union
from pydantic import BaseModel


class cdfSource(BaseModel):
    source_type: str
    repo_name: str
    branch: str

class Assume_role(BaseModel):
    role: str


class cdfDeploymentcfn(BaseModel):
    assume_role: Assume_role
    aws_account: str
    region: str
    type: Literal["cfn"]
    parameters: Optional[str]
    capabilities: Optional[str]
    deployment_file: str
    iam_policy_file: str
    checks: List[str]

class cdfDeploymentTerraform(BaseModel):
    assume_role: Assume_role
    aws_account: str
    region: str
    type: Literal["terraform"]
    parameters: Optional[str]
    deployment_folder: str
    iam_policy_file: str
    checks: List[str]


class cdfPipeline(BaseModel):
    name: str
    provider: str
    source: cdfSource
    deployment: Union[cdfDeploymentcfn , cdfDeploymentTerraform]
