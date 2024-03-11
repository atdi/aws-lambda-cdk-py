#!/usr/bin/env python3

import aws_cdk as cdk
from stacks.api_stack import DemoStack

if __name__ == "__main__":
    app = cdk.App()
    application_stack = DemoStack(app, 'DemoStack')
    app.synth()
