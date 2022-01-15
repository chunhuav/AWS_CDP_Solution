#!/usr/bin/env python3

import aws_cdk as cdk

from cdp_solution_2.cdp_solution_2_stack import CdpSolution2Stack


app = cdk.App()
# Get all the variables from the cdk.json file
# env_US = cdk.Environment(account="22", region="us-east-1")
# env_Tokyo = cdk.Environment(account="23", region="ap-northeast-1")

CdpSolution2Stack(app, "CdpSolution2Stack")

# MyDevStack(app, "dev", env=cdk.Environment(
#     account=os.environ.get("CDK_DEPLOY_ACCOUNT", os.environ["CDK_DEFAULT_ACCOUNT"]),
#     region=os.environ.get("CDK_DEPLOY_REGION", os.environ["CDK_DEFAULT_REGION"])

app.synth()

