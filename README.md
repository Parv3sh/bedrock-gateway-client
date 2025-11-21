# Bedrock Gateway Client

[![PyPI version](https://badge.fury.io/py/bedrock-gateway-client.svg)](https://pypi.org/project/bedrock-gateway-client/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/Parv3sh/bedrock-gateway-client.svg)](https://github.com/Parv3sh/bedrock-gateway-client/stargazers)
[![Downloads](https://pepy.tech/badge/bedrock-gateway-client)](https://pepy.tech/project/bedrock-gateway-client)

A Python client for AWS Bedrock Gateway with IAM authentication. Works with any private API Gateway setup for AWS Bedrock, featuring both Python API and CLI interface.

## Features

- ✅ **Configurable** - Works with any Bedrock Gateway deployment
- ✅ **No secrets required** - Uses your AWS IAM credentials
- ✅ **Simple API** - Just `client.chat("message")`
- ✅ **Multiple configuration methods** - Constructor, environment variables, or config file
- ✅ **CLI included** - Command-line interface for quick testing

## Installation

```bash
pip install bedrock-gateway-client==1.0.3
```

Requirements:
- Python 3.8+
- boto3>=1.26.0
- requests>=2.28.0
- pyyaml>=6.0
- click>=8.0.0

## Quick Start

### Python API

```python
from bedrock_gateway_client import BedrockClient

client = BedrockClient(
    gateway_url="https://your-api-gateway.execute-api.region.amazonaws.com/prod/invoke",
    api_id="your-api-id",  # Your API Gateway ID
    region="your-region"
)

response = client.chat("Tell me about koalas")
print(response.text)
print(f"Tokens used: {response.tokens}")
```

### CLI Interface

```bash
# Configure once
bedrock-gateway configure --gateway-url "https://your-api-gateway.execute-api.region.amazonaws.com/prod/invoke" --api-id "your-api-id" --region your-region

# Chat with Claude
bedrock-gateway chat "Tell me about koalas"
```

## Configuration Options

### Direct Configuration

```python
from bedrock_gateway_client import BedrockClient

client = BedrockClient(
    gateway_url="https://your-api-gateway.execute-api.region.amazonaws.com/prod/invoke",
    api_id="your-api-id",  # Your API Gateway ID
    region="your-region"
)
```

### Environment Variables

```bash
export BEDROCK_GATEWAY_URL="https://your-api-gateway.execute-api.region.amazonaws.com/prod/invoke"
export BEDROCK_GATEWAY_API_ID="your-api-id"
export BEDROCK_GATEWAY_REGION="your-region"
```

```python
from bedrock_gateway_client import BedrockClient

client = BedrockClient()  # Uses environment variables
```

### CLI Configuration

```bash
# Save configuration to file
bedrock-gateway configure \
  --gateway-url "https://your-api-gateway.execute-api.region.amazonaws.com/prod/invoke" \
  --api-id "your-api-id" \
  --region your-region
```

### Global Configuration

```python
from bedrock_gateway_client import configure, chat

configure(
    gateway_url="https://your-api-gateway.execute-api.region.amazonaws.com/prod/invoke",
    api_id="your-api-id",
    region="your-region",
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
# Show help
bedrock-gateway --help

# Configure your Bedrock Gateway
bedrock-gateway configure \
  --gateway-url "https://your-api-gateway.execute-api.region.amazonaws.com/prod/invoke" \
  --api-id "your-api-id" \
  --region your-region

# Chat with Claude
bedrock-gateway chat "Tell me about koalas"

# Advanced chat with options
bedrock-gateway chat "Explain quantum computing" \
  --model sonnet-4.5 \
  --max-tokens 1000

# Check your AWS identity
bedrock-gateway whoami
```

### Available Models
- `sonnet-4.5` - Best for detailed, complex conversations
- `haiku-4.5` - Fast and efficient for simple tasks

### Configuration File
Configuration is saved to `~/.bedrock-gateway/config.yaml`:

```yaml
api_id: your-api-id
gateway_url: https://your-api-gateway.execute-api.region.amazonaws.com/prod/invoke
region: your-region
model_map:
  sonnet-4.5: anthropic.claude-sonnet-4-5-v1:0
  haiku-4.5: anthropic.claude-haiku-4-5-v1:0
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

## Troubleshooting

### Common Issues

**1. 403 Forbidden Error**
If you get a 403 Forbidden error, check:
- Your AWS credentials have the required permissions
- The API Gateway resource policy allows your role
- Both `gateway_url` and `api_id` are configured correctly

```bash
# Verify configuration
bedrock-gateway whoami

# Test with verbose output
bedrock-gateway chat "Hello" --verbose
```

**2. Authentication Errors**
Ensure your AWS credentials are properly configured:

```bash
# Check AWS credentials
aws sts get-caller-identity

# Configure AWS credentials if needed
aws configure
```

**3. Gateway Not Found**
Make sure both `gateway_url` and `api_id` are set correctly in your configuration.

## Authentication

Uses your AWS credentials automatically:

- Default AWS credentials (~/.aws/credentials)
- AWS profile: `BedrockClient(profile="my-profile")`
- Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
- IAM role (when running on EC2/Lambda/ECS)

### Required AWS Permissions

Your IAM role needs these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "execute-api:Invoke"
      ],
      "Resource": "arn:aws:execute-api:region:account-id:your-api-id/*/*"
    }
  ]
}
```

## License

MIT License - see LICENSE file for details

## Support

For issues, open a GitHub issue at:
<https://github.com/parv3sh/bedrock-gateway-client/issues>
