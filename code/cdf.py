#!/usr/bin/env python3
import json
import aws_cdk as cdk
from code.pipeline import build_pipeline
from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    SecretValue,
)

class cdf(Stack):

    def __init__(self, config_file: str, definitions_file: str, **kwargs) -> None:
        super().__init__(**kwargs)

        app = cdk.App()

        config = self.import_json_file(config_file)
        definitions = self.import_json_file(definitions_file)

        for pipeline in config['pipelines']:
            # Import Iam policy file
            iam_policy_file = pipeline['deployment']['iam_policy_file']
            iam_policy = self.import_json_file(iam_policy_file)
            
            # Build a pipeline
            build_pipeline(app, "cdf-" + pipeline['name'], pipeline, definitions, iam_policy)
        app.synth()
        
    def import_json_file(self, file: str):
        # TODO: Verify conf.d/config.yaml
        # TODO: Run pre-checks such as validating Github creds
        with open(file, "r") as file_object:
            file_json = json.load(file_object)

        return file_json