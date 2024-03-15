import aws_cdk as cdk
from aws_cdk import (aws_lambda as lambda_,
                     aws_iam as iam,
                     aws_apigateway as apigateway,
                     aws_s3 as s3,
                     aws_s3_deployment as s3deploy
                     )
import boto3


class DemoStack(cdk.Stack):
    def __init__(self, scope: cdk, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        bucket = s3.Bucket.from_bucket_name(
            self,
            id="DeploymentBucket",
            bucket_name="eu-aagsolutions-demo-stack"
        )

        bucket_deployment = s3deploy.BucketDeployment(self, "DeployFunction",
                                                      sources=[s3deploy.Source.asset(
                                                          "build/")],
                                                      destination_bucket=bucket,
                                                      destination_key_prefix="api")
        s3_client = boto3.client('s3')

        response = s3_client.list_object_versions(
            Bucket="eu-aagsolutions-demo-stack",
            Prefix="api/lambda.zip"
        )
        latest_version = [d for d in response['Versions'] if d['IsLatest'] is True][0]['VersionId']
        rest_lambda_role = iam.Role(self, id="RestLambdaRole",
                                    assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
                                    managed_policies=[
                                        iam.ManagedPolicy.from_aws_managed_policy_name(
                                            "service-role/AWSLambdaBasicExecutionRole")
                                    ],
                                    # Inline Policies go here
                                    )
        rest_lambda_function = lambda_.Function(self, "RestAPI",
                                                handler="app_api.handle",
                                                runtime=lambda_.Runtime.PYTHON_3_12,
                                                timeout=cdk.Duration.seconds(300),
                                                code=lambda_.Code.from_bucket(
                                                    bucket=bucket,
                                                    key='api/lambda.zip',
                                                    object_version=latest_version),
                                                role=rest_lambda_role,
                                                environment={})
        api = apigateway.LambdaRestApi(
            self, 'Endpoint',
            handler=rest_lambda_function,
        )
        api.root.add_resource('api').add_resource('demo').add_method('GET',
                                                                     apigateway.LambdaIntegration(rest_lambda_function))
