#!/usr/bin/env python3
import json
from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codecommit as codecommit,
    aws_iam as iam,
    aws_s3 as s3,
    SecretValue,
)
from typing import List, Dict

class build_pipeline(Stack):

    def __init__(self, scope: Construct, construct_id: str, pipeline, definitions, iam_policy, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Set parameters
        self.pipeline = pipeline
        self.definitions = definitions
        self.iam_policy = iam_policy

        #TODO:
        # Run the pipelines
        # Verify results 
        
        # Build Buckets
        reports_bucket = s3.Bucket(self, "reportsbucket")
        source_bucket = s3.Bucket(self, "sourcebucket")
       
        # Build Pipeline Stages
        stages = self.set_stages()

        # Build Pipeline
        codepipeline.Pipeline(self, pipeline['name'],
            stages=stages
        )
        #END of init
        
    def set_stages(self) -> List[codepipeline.StageProps]:
        
        # Set source
        repo_name = self.pipeline['source']['repo_name']
        repository = codecommit.Repository.from_repository_name(self, repo_name,
            repository_name=repo_name
        )
        source_output = codepipeline.Artifact()
        branch_name = self.pipeline['source']['branch']
        source_action = codepipeline_actions.CodeCommitSourceAction(
            action_name="CodeCommit",
            repository=repository,
            branch=branch_name,
            output=source_output
        )

        # Initialize stages and add source stage
        stages=[
            codepipeline.StageProps(
                stage_name="Source",
                actions=[source_action]
                )
        ]

        # Build Codebuild Role
        # TODO: Add support for Conditions
        pipeline_name = self.pipeline['name']
        codebuild_role = iam.Role(self, "codebuild_Role_" + pipeline_name,
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com")
        )

        for statement in self.iam_policy['Statement']:
            effect = iam.Effect.ALLOW
            if statement['Effect'] == "Deny":
                effect = iam.Effect.DENY

            codebuild_role.add_to_policy(iam.PolicyStatement(
                resources=[statement['Resource']],
                actions=[statement['Action']],
                effect=effect
                )
            )

        # Create codebuild_project_image
        codebuild_project_image = codebuild.LinuxBuildImage.from_asset(self, "base-image", directory="images/base-image")

        # Get projects_definition 
        projects_definition = self.definitions['deployment'][self.pipeline['deployment']['type']]

        # Loop over projects_definition to create CodeBuild Projects
        for project in projects_definition:
            # Create BuildSpec
            buildspec = self.generate_buildspec(project, self.pipeline)
            # print("Buildspec:")
            # print(json.dumps(buildspec, indent=4))

            # CodeBuild Project:
            build_project = codebuild.PipelineProject(self, "codebuild_" + project['project_name'],
                build_spec=codebuild.BuildSpec.from_object(buildspec),
                role=codebuild_role,
                environment=codebuild.BuildEnvironment(
                    build_image = codebuild_project_image,
                ),
                environment_variables={
                    "PIPELINE": codebuild.BuildEnvironmentVariable(value=json.dumps(self.pipeline))
                    }
            )

            build_action = codepipeline_actions.CodeBuildAction(
                action_name="CodeBuild",
                project=build_project,
                input=source_output,
                outputs=[codepipeline.Artifact()],  # optional
                combine_batch_build_artifacts=True
            )
            
            # Adding CodeBuild stages to Stages
            codebuild_stage = codepipeline.StageProps(
                stage_name=project['project_name'],
                actions=[build_action]
                )
            stages.append(codebuild_stage)
        
        return stages

    def generate_buildspec(self, project, pipeline) -> Dict[str, any]:
        # Initializations
        buildspec = {
            "version"   : "0.2",
            "phases"    : {
                "install"       : {"commands" : []},
                "pre_build"     : {"commands" : []},
                "build"         : {"commands" : []},
                "post_build"    : {"commands" : []}
                }
            }

        # Adding deployment Phases: All Phses
        for command in project['build_spec_phases']['install']:
            buildspec['phases']['install']['commands'].append(command)
        for command in project['build_spec_phases']['pre_build']:
            buildspec['phases']['pre_build']['commands'].append(command)
        for command in project['build_spec_phases']['build']:
            buildspec['phases']['build']['commands'].append(command)
        for command in project['build_spec_phases']['post_build']:
            buildspec['phases']['post_build']['commands'].append(command)

        # Adding Checks stages: install, pre_build, and post_build
        if project['security_checks'] == "true":
            for check in pipeline['deployment']['checks']:
                try: 
                    if self.definitions['checks'][check].__str__:
                        for command in self.definitions['checks'][check]['install']:
                            buildspec['phases']['install']['commands'].append(command)
                        for command in self.definitions['checks'][check]['pre_build']:
                            buildspec['phases']['pre_build']['commands'].append(command)
                        for command in self.definitions['checks'][check]['post_build']:
                            buildspec['phases']['post_build']['commands'].append(command)
                except:
                    print("Check: ", check, "is not defined")
        return buildspec
