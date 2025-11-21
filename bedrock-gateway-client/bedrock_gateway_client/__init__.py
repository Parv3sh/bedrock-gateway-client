"""
AWS Bedrock Gateway Client
===========================

A Python client for private AWS Bedrock gateways with IAM authentication.

Usage:
    from bedrock_gateway_client import BedrockClient
    
    client = BedrockClient(
        gateway_url="https://your-api-gateway.execute-api.region.amazonaws.com/prod/invoke",
        region="ap-southeast-2"
    )
    
    response = client.chat("Tell me about koalas")
    print(response.text)
"""

from .client import BedrockClient, BedrockResponse, chat, configure
from .config import Config

__version__ = "1.0.0"
__all__ = ["BedrockClient", "BedrockResponse", "chat", "configure", "Config"]
