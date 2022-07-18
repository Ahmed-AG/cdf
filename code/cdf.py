import json
from typing import Dict
import aws_cdk as cdk
from code.build_codepipeline import build_codepipeline
from code.data_types.pipeline import *
from code.data_types.iam_role import *
from code.data_types.definitions import *
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
        try:
            validation = validate_definitions(definitions)
            if validation:
                raise Exception(f"Definitions configuration is not valid: {validation}")
        except KeyError as e:
            raise KeyError(f"Definitions configuration is missing key {e}") from e
        definitions = Definitions.from_json(json.dumps(definitions))

        for pipeline in config['pipelines']:
            # Validate every pipeline configuration
            try:
                validation = validate_pipeline_config(pipeline)
                if validation:
                    raise Exception(f"Pipeline configuration is not valid: {validation}")
            except KeyError as e:
                raise KeyError(f'Pipeline configuration is missing key {e}') from e
            pipeline = Pipeline.from_json(json.dumps(pipeline))
            
            # Create BuildSpec
            buildspec = self.generate_buildspec(pipeline, definitions)
            print(json.dumps(buildspec, indent=4))

            # Create IAM Statement
            iam_policy_file = pipeline.deployment.iam_policy_file
            iam_policy = self.import_json_file(iam_policy_file)

            try:
                validation = validate_iam_policy(iam_policy)
                if validation:
                    raise Exception(f"Iam policy configuration is not valid: {validation}")
            except KeyError as e:
                raise KeyError(f'Iam Policy is missing key {e}') from e

            iam_policy = Iam_policy.from_json(json.dumps(iam_policy))
            
            # Build Pipeline
            build_codepipeline(app, "cdf-" + pipeline.name, pipeline, buildspec, iam_policy)
        app.synth()
        
    def import_json_file(self, file: str) -> object:
        # TODO: Verify conf.d/config.yaml
        # TODO: Run pre-checks such as validating Github creds
        with open(file, "r") as file_object:
            file_json = json.load(file_object)    
        return file_json

    def generate_buildspec(self, pipeline: Pipeline, definitions: Definitions) -> Dict[str, any]:
        # Initializations
        install_stage = {"commands" : []}
        pre_build_stage = {"commands" : []}
        build_stage = {"commands" : []}
        post_build_stage = {"commands" : []}

        # Creating install, pre_build, and post_build stages        
        for check in pipeline.deployment.checks:
            try:
                if definitions.checks.get(check).__str__:
                    for command in definitions.checks.get(check).install:
                        install_stage['commands'].append(command)
                    for command in definitions.checks.get(check).pre_build:
                        pre_build_stage['commands'].append(command)
                    for command in definitions.checks.get(check).post_build:
                        post_build_stage['commands'].append(command)
            except:
                print("Check: ", check, "is not defined")

        # Creating build stage
        try:
            if definitions.deployment.get(pipeline.deployment.type).build.__str__:
                for command in definitions.deployment.get(pipeline.deployment.type).build:
                    build_stage['commands'].append(command)
        except:
            print("Deployment definitions error!")    

        # Build phases JSON object
        phases = {
            "install"       : install_stage,
            "pre_build"     : pre_build_stage,
            "build"         : build_stage,
            "post_build"    : post_build_stage
            }

        # Build final buildspec JSON object
        buildspec = {
                "version"   : "0.2",
                "phases"    : phases
                }
        
        return buildspec