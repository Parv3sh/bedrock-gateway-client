# Bedrock Gateway Client

[![PyPI version](https://badge.fury.io/py/bedrock-gateway-client.svg)](https://pypi.org/project/bedrock-gateway-client/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/Parv3sh/bedrock-gateway-client.svg)](https://github.com/Parv3sh/bedrock-gateway-client/stargazers)
[![Downloads](https://pepy.tech/badge/bedrock-gateway-client)](https://pepy.tech/project/bedrock-gateway-client)

A Python client for AWS Bedrock Gateway with IAM authentication. Works with any private API Gateway setup for AWS Bedrock.

## Features

- ✅ **Configurable** - Works with any Bedrock Gateway deployment
- ✅ **No secrets required** - Uses your AWS IAM credentials
- ✅ **Simple API** - Just `client.chat("message")`
- ✅ **Multiple configuration methods** - Constructor, environment variables, or config file
- ✅ **CLI included** - Command-line interface for quick testing

## Installation

```bash
pip install bedrock-gateway-client
```

## Quick Start

```python
from bedrock_gateway_client import BedrockClient

client = BedrockClient(
    gateway_url="https://your-api-gateway.execute-api.region.amazonaws.com/prod/invoke",
    region="us-east-1"
)

response = client.chat("Tell me about koalas")
print(response.text)
print(f"Tokens used: {response.tokens}")
```

## Configuration Options

### Direct Configuration

```python
from bedrock_gateway_client import BedrockClient

client = BedrockClient(
    gateway_url="https://your-gateway.execute-api.region.amazonaws.com/prod/invoke",
    region="us-east-1"
)
```

### Environment Variables

```bash
export BEDROCK_GATEWAY_URL="https://your-gateway.execute-api.region.amazonaws.com/prod/invoke"
export BEDROCK_GATEWAY_REGION="us-east-1"
```

```python
from bedrock_gateway_client import BedrockClient

client = BedrockClient()  # Uses environment variables
```

### Global Configuration

```python
from bedrock_gateway_client import configure, chat

configure(
    gateway_url="https://your-gateway.execute-api.region.amazonaws.com/prod/invoke",
    region="us-east-1",
    save=True
)

# Now use simple chat function
response = chat("Tell me about koalas")
print(response)
```

## Usage Examples

### Basic Chat

```python
response = client.chat(
    "What is AWS Bedrock?",
    model="sonnet-4.5",
    max_tokens=500
)

print(response.text)
print(f"Tokens: {response.tokens}")
print(f"Latency: {response.latency_ms}ms")
```

### With System Prompt

```python
response = client.chat(
    "What is 2+2?",
    system="You are a helpful math tutor.",
    model="sonnet-4.5"
)
```

### Multi-turn Conversation

```python
# First turn
response1 = client.chat("My name is Alice")

# Build history
history = [
    {"role": "user", "content": [{"text": "My name is Alice"}]},
    {"role": "assistant", "content": [{"text": response1.text}]}
]

# Second turn with context
response2 = client.chat(
    "What's my name?",
    conversation_history=history
)
```

## Command-Line Interface

```bash
# Configure
bedrock-gateway configure --gateway-url "https://..." --region us-east-1

# Chat
bedrock-gateway chat "Tell me about AWS Bedrock" --model sonnet-4.5

# Check identity
bedrock-gateway whoami
```

## Response Object

```python
response.text           # The generated text
response.tokens         # Total tokens used
response.input_tokens   # Input tokens
response.output_tokens  # Output tokens
response.latency_ms     # Response time in milliseconds
response.request_id     # Unique request ID
response.model          # Model used
response.stop_reason    # Why generation stopped
response.raw_response   # Full raw response
```

## Authentication

Uses your AWS credentials automatically:
- Default AWS credentials (~/.aws/credentials)
- AWS profile: `BedrockClient(profile="my-profile")`
- Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
- IAM role (when running on EC2/Lambda/ECS)

## License

MIT License - see LICENSE file for details

## Support

For issues, open a GitHub issue at:
https://github.com/parv3sh/bedrock-gateway-client/issues
