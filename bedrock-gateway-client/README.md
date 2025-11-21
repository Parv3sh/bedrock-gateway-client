# Bedrock Gateway Client

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

## Roy Morgan Setup

If you're at Roy Morgan, configure once:

```python
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
```

Then use:

```python
from bedrock_gateway_client import chat
print(chat("Tell me about koalas"))
```

## License

MIT License - see LICENSE file for details

## Support

For issues, open a GitHub issue at:
https://github.com/parveshh/bedrock-gateway-client/issues
