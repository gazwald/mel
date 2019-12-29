#!/usr/bin/env python3
import os

from aws_cdk import core

from deploy.deploy_stack import DeployStack

env = {'account': os.getenv('AWS_ACCOUNT', os.getenv('CDK_DEFAULT_ACCOUNT', '')),
       'region': 'us-west-2'}

app = core.App()
DeployStack(app, "deploy", env=env)

app.synth()
