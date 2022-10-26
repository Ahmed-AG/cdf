#!/usr/bin/env python3
import json
import aws_cdk as cdk
from code.pipeline import build_pipeline
from code.data_structures import (
    cdfPipeline,
    cdfDefinitions,
    cdfIamPolicy
)
from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    SecretValue,
)

def app(config_file: str, definitions_file: str) -> None:
    app: Construct = cdk.App()
    cdf(app, config_file, definitions_file)
    app.synth()

class cdf(Stack):

    def __init__(self, app: Construct, config_file: str, definitions_file: str, **kwargs) -> None:
        super().__init__(**kwargs)
        
        app = app

        config: dict = self.import_json_file(config_file)
        definitions_config: dict = self.import_json_file(definitions_file)
        definitions: cdfDefinitions = self.make_definitions(definitions_config)

        for pipeline_config in config['pipelines']:

            pipeline: cdfPipeline = self.make_pipeline(pipeline_config)
            # Import Iam policy file

            iam_policy_file: str = pipeline.deployment.iam_policy_file
            iam_policy_config: dict = self.import_json_file(iam_policy_file)
            
            iam_policy: cdfIamPolicy = self.make_iam_policy(iam_policy_config)
            # Build a pipeline
            build_pipeline(app, "cdf-" + pipeline.name, pipeline, definitions, iam_policy)

    def make_definitions(self, json_config: dict) -> cdfDefinitions:
        definitions: cdfDefinitions = cdfDefinitions.parse_obj(json_config)
        return definitions

    def make_pipeline(self, json_config: dict) -> cdfPipeline:
        pipeline: cdfPipeline = cdfPipeline.parse_obj(json_config)
        return pipeline

    def make_iam_policy(self, json_config: dict) -> cdfIamPolicy:
        policy: cdfIamPolicy = cdfIamPolicy.parse_obj(json_config)
        return policy

    def import_json_file(self, file: str) -> dict:
        # TODO: Verify conf.d/config.yaml
        # TODO: Run pre-checks such as validating Github creds
        with open(file, "r") as file_object:
            file_json = json.load(file_object)

        return file_json