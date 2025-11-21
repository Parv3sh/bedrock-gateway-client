#!/usr/bin/env python3
"""Roy Morgan specific setup"""

from bedrock_gateway_client import configure

configure(
    gateway_url="https://vpce-03162ee3093fbd956-w5fiddec.execute-api.ap-southeast-2.vpce.amazonaws.com/prod/invoke",
    region="ap-southeast-2",
    model_map={
        'sonnet-4.5': 'au.anthropic.claude-sonnet-4-5-20250929-v1:0',
        'haiku-4.5': 'au.anthropic.claude-haiku-4-5-20251001-v1:0',
    },
    save=True
)

print("✅ Configured for Roy Morgan's Bedrock Gateway")
