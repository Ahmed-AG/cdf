# Cloud Deployment Framework (CDF) - Beta
## Overview
Cloud Deployment Framework (CDF) provides an automated, cloud native, and secure way to deploy cloud resources. 
Based on JSON configuration files, CDF uses AWS CDK to automatically create Codepipeline Pipelines that clone repos, run secrutiy checks on code, and deploy resources. It will also build any needed docker containers for Codebuild Projects

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
 2. rename `config.d.templates` to `config.d`
 2. Edit `config.d/config.json`: Set pipelines names, sources, deployment options, and any parameters needed

```bash
{
    "pipelines" :[
        {
            "name" : "Production-Pipeline1",
            "provider" : "aws",
            "source" : {
                "source_type" : "codecommit",
                "repo_name" : "big_infra",
                "branch" : "main"
            },
            "parameters" : {
            },
            "deployment" : {
                "aws_account" : "************",
                "region" : "us-east-1",
                "type" : "cfn",
                "deployment_file" : "main.yaml",
                "checks" : [
                    "cfn_nag", 
                    "checkov" 
                ]
            }
        }
    ]
}
```
3. Run:
```bash
cdk deploy --all
```
4. Check Codepipline in AWS console

## Support
To report a bug, request a feature, or submit a suggestion/feedback, please submit an issue through the GitHub repository: https://github.com/Ahmed-AG/cdf/issues/new