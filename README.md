# Cloud Deployment Framework (CDF) - Beta
## Overview
Cloud Deployment Framework (CDF) provides an automated, cloud native, and secure way to deploy cloud resources. 
Based on JSON configuration files, CDF uses AWS CDK to automatically create Codepipeline Pipelines that clone repos, run secrutiy checks on code, and deploy resources. It will also build any needed docker containers for Codebuild Projects

![alt text](https://github.com/Ahmed-AG/cdf/blob/main/cdf.jpg?raw=true)

## Supported tools
### Deployment tools
Infrastructure as Code Tools  | Link |
--- | --- |
Cloud Formation | https://aws.amazon.com/cloudformation/
Terraform (Coming soon) | https://www.terraform.io

### Security testing tools
Tools | Description | Link |
--- | --- | --- |
cfn_nag | The cfn-nag tool looks for patterns in CloudFormation templates that may indicate insecure infrastructure | https://github.com/stelligent/cfn_nag
checkov (Coming soon) | Checkov uses a common command line interface to manage and analyze infrastructure as code (IaC) scan results across platforms such as Terraform, CloudFormation, Kubernetes, Helm, ARM Templates and Serverless framework | https://www.checkov.io
Semgrep (Coming soon) | Static analysis at ludicrous speed Find bugs and enforce code standards | https://semgrep.dev

## Requirements
You will need the following on your local machine:
1. Python3
2. awscli
3. cdk: run the Bootstrapping process four at https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html
```bash
cdk bootstrap aws://ACCOUNT-NUMBER-1/REGION-1
```
4. docker

## Usage
 1. Clone the repo
 2. Rename `config.d.templates` to `config.d`
 3. Edit `config.d/config.json` to set pipelines names, sources, deployment options, and any parameters needed

Sample config.json file:

```bash
{
    "pipelines" :[
        {
            "name" : "Production-Pipeline1",
            "provider" : "aws",
            "source" : {
                "source_type" : "codecommit",
                "repo_name" : "cdf-repo1",
                "branch" : "main"
            },
            "deployment" : {
                "assume_role" :{
                    "role": "TODO"
                },
                "aws_account" : "",
                "iam_policy_file" : "config.d/iam-policy.json",
                "region" : "us-east-1",
                "type" : "cfn",
                "parameters" : "VpcCIDR=10.0.0.0/16 Region=$REGION",
                "capabilities" : "CAPABILITY_IAM CAPABILITY_NAMED_IAM",
                "deployment_file" : "main.yaml",
                "checks" : [
                    "general_all",
                    "cfn_nag", 
                    "checkov"
                ]
            }
        }
    ]
}
```
4. Edit the IAM policy file used by the pipeline to deploy resources `config.d/iam-policy.json`
   Note: This file is referenced in `config.d/config.json`. It is recomended to have different policies for each pipeline

5. Run:
```bash
cdk deploy --all
```
6. Verify that your pipelines were created in Codepipline in AWS console

## Support
To report a bug, request a feature, or submit a suggestion/feedback, please submit an issue through the GitHub repository: https://github.com/Ahmed-AG/cdf/issues/new