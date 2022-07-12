import json
import aws_cdk as cdk
from code.build_codepipeline import build_codepipeline
from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    SecretValue,
)

class cdf(Stack):

    def __init__(self, config_file, definitions_file, **kwargs) -> None:
        super().__init__(**kwargs)

        app = cdk.App()

        config = self.import_json_file(config_file)
        definitions = self.import_json_file(definitions_file)

        for pipeline in config['pipelines']:

            # Create BuildSpec
            buildspec = self.generate_buildspec(pipeline, definitions )
            print(json.dumps(buildspec, indent=4))

            # Build Pipeline
            build_codepipeline(app, "cdf-" + pipeline['name'], pipeline, buildspec)
        
        app.synth()
        
    def import_json_file(self, file):
        # TODO: Verify conf.d/config.yaml
        # TODO: Run pre-checks such as validating Github creds
        file_object = open(file)
        file_json = json.load(file_object)

        return file_json

    def generate_buildspec(self, pipeline, definitions):
        # Initializations
        install_stage = {"commands" : []}
        pre_build_stage = {"commands" : []}
        build_stage = {"commands" : []}
        post_build_stage = {"commands" : []}

        # Creating install, pre_build, and post_build stages
        for check in pipeline['deployment']['checks']:
            try: 
                if definitions['checks'][check].__str__:
                    for command in definitions['checks'][check]['install']:
                        install_stage['commands'].append(command)
                    for command in definitions['checks'][check]['pre_build']:
                        pre_build_stage['commands'].append(command)
                    for command in definitions['checks'][check]['post_build']:
                        post_build_stage['commands'].append(command)
            except:
                print("Check: ", check, "is not defined")
        
        # Creating build stage
        try: 
            if definitions['deployment'][pipeline['deployment']['type']]['build'].__str__:
                for command in  definitions['deployment'][pipeline['deployment']['type']]['build']:
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