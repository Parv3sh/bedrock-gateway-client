"""Command-line interface for Bedrock Gateway Client"""

import click
from .client import BedrockClient
from .config import Config


@click.group()
def cli():
    """Bedrock Gateway Client CLI"""
    pass


@cli.command()
@click.option('--gateway-url', help='Gateway URL')
@click.option('--api-id', help='API Gateway ID')
@click.option('--region', default='us-east-1', help='AWS region')
@click.option('--profile', help='AWS profile')
def configure(gateway_url, api_id, region, profile):
    """Configure the Bedrock Gateway client"""
    from . import configure as config_func
    
    config_func(
        gateway_url=gateway_url,
        api_id=api_id,
        region=region,
        profile=profile,
        save=True
    )
    
    click.echo("✅ Configuration saved!")


@cli.command()
@click.argument('message')
@click.option('--model', default='sonnet-4.5', help='Model to use')
@click.option('--max-tokens', default=2000, help='Maximum tokens')
def chat(message, model, max_tokens):
    """Send a chat message"""
    client = BedrockClient(verbose=True)
    response = client.chat(message, model=model, max_tokens=max_tokens)
    
    click.echo()
    click.echo(response.text)
    click.echo()
    click.echo(f"📊 Tokens: {response.tokens} | ⚡ Latency: {response.latency_ms}ms")


@cli.command()
def whoami():
    """Show your AWS identity"""
    client = BedrockClient(verbose=True)
    click.echo(f"User ARN: {client.user_arn}")


if __name__ == '__main__':
    cli()
