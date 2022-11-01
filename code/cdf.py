#!/usr/bin/env python3
import json
import aws_cdk as cdk
from code.build_pipeline import build_pipeline
from code.iam.policy import (
    cdfIamPolicy,
    parse_cdfIamPolicy
)
from code.definitions import (
    cdfDefinitions,
    parse_cdfDefinitions
)
from code.pipeline import (
    cdfPipeline,
    parse_cdfPipeline
)
from code.utilities import (
    import_json_file
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

        config: dict = import_json_file(config_file)
        definitions_config: dict = import_json_file(definitions_file)
        definitions: cdfDefinitions = parse_cdfDefinitions(definitions_config)

        for pipeline_config in config['pipelines']:

            pipeline: cdfPipeline = parse_cdfPipeline(pipeline_config)
            # Import Iam policy file

            iam_policy_file: str = pipeline.deployment.iam_policy_file
            iam_policy_config: dict = import_json_file(iam_policy_file)
            
            iam_policy: cdfIamPolicy = parse_cdfIamPolicy(iam_policy_config)
            # Build a pipeline
            build_pipeline(app, "cdf-" + pipeline.name, pipeline, definitions, iam_policy)
