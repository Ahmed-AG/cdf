import json
from constructs import Construct
from code.custom_dataclasses import Pipeline, Iam_policy
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
    aws_s3 as s3,
    SecretValue,
)

class build_codepipeline(Stack):

    def __init__(self, scope: Construct, construct_id: str, pipeline: Pipeline, buildspec, iam_policy: Iam_policy, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #TODO:
        # Run the pipelines
        # Verify results 
        
        reports_bucket = s3.Bucket(self, "reportsbucket")
        source_bucket = s3.Bucket(self, "sourcebucket")

        repository = codecommit.Repository.from_repository_name(self, pipeline.source.repo_name,
            repository_name=pipeline.source.repo_name
        )
        
        source_output = codepipeline.Artifact()
        
        source_action = codepipeline_actions.CodeCommitSourceAction(
            action_name="CodeCommit",
            repository=repository,
            branch=pipeline.source.branch,
            output=source_output
        )

        codebuild_role = iam.Role(self, "codebuild_Role_" + pipeline.name,
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com")
        )
        # TODO: Add support for Conditions
        
        for statement in iam_policy.Statement:
            # print(statement)

            effect = iam.Effect.ALLOW
            if statement.Effect == "Deny":
                effect = iam.Effect.DENY

            codebuild_role.add_to_policy(iam.PolicyStatement(
            resources=[statement.Resource],
            actions=[statement.Action],
            effect=effect
        ))
        # Old code        
        # codebuild_role.add_to_policy(iam.PolicyStatement(
        #     resources=["*"],
        #     actions=["*"]
        # ))

        project = codebuild.PipelineProject(self, "codebuild_" + pipeline.name,
            build_spec=codebuild.BuildSpec.from_object(buildspec),
            role=codebuild_role,
            environment=codebuild.BuildEnvironment(
                build_image = codebuild.LinuxBuildImage.from_asset(self, "base-image", directory="images/base-image"),
            ),
            environment_variables={
                "PIPELINE": codebuild.BuildEnvironmentVariable(value=json.dumps(pipeline.to_json()))
                }
        )

        build_action = codepipeline_actions.CodeBuildAction(
            action_name="CodeBuild",
            project=project,
            input=source_output,
            outputs=[codepipeline.Artifact()],  # optional
            combine_batch_build_artifacts=True
        )

        codepipeline.Pipeline(self, pipeline.name,
            stages=[codepipeline.StageProps(
                stage_name="Source",
                actions=[source_action]
            ), codepipeline.StageProps(
                stage_name="Build",
                actions=[build_action]
            )
            ]
        )

