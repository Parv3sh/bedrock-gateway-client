"""Bedrock Gateway Client"""

import boto3
import json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import requests

from .config import Config


@dataclass
class BedrockResponse:
    """Response from Bedrock Gateway"""
    text: str
    tokens: int
    input_tokens: int
    output_tokens: int
    latency_ms: int
    request_id: str
    model: str
    stop_reason: str
    raw_response: Dict[str, Any]
    
    def __str__(self):
        return self.text
    
    def __repr__(self):
        return f"BedrockResponse(tokens={self.tokens}, latency={self.latency_ms}ms)"


class BedrockClient:
    """Client for AWS Bedrock Gateway with IAM authentication"""
    
    def __init__(
        self,
        gateway_url: Optional[str] = None,
        api_id: Optional[str] = None,
        region: Optional[str] = None,
        profile: Optional[str] = None,
        config: Optional[Config] = None,
        verbose: bool = False
    ):
        """Initialize Bedrock Gateway client"""
        
        if config is None:
            try:
                config = Config.from_file()
            except:
                config = Config()
            
            env_config = Config.from_env()
            if env_config.gateway_url:
                config.gateway_url = env_config.gateway_url
            if env_config.api_id:
                config.api_id = env_config.api_id
            if env_config.region != 'us-east-1':
                config.region = env_config.region
            if env_config.aws_profile:
                config.aws_profile = env_config.aws_profile
            
            if gateway_url:
                config.gateway_url = gateway_url
            if api_id:
                config.api_id = api_id
            if region:
                config.region = region
            if profile:
                config.aws_profile = profile
            if verbose:
                config.verbose = verbose
        
        self.config = config
        
        try:
            self.gateway_url = self.config.get_full_url()
            self.host = self.config.get_host()
        except ValueError as e:
            raise ValueError(
                f"{str(e)}\n\n"
                "Configuration options:\n"
                "1. Pass gateway_url or api_id to constructor\n"
                "2. Set BEDROCK_GATEWAY_URL or BEDROCK_GATEWAY_API_ID environment variable\n"
                "3. Create config file: ~/.bedrock-gateway/config.yaml\n"
            )
        
        self.session = boto3.Session(profile_name=self.config.aws_profile)
        self.credentials = self.session.get_credentials()
        
        if not self.credentials:
            raise Exception(
                "No AWS credentials found. Please configure your AWS credentials.\n"
                "Run: aws configure"
            )
        
        try:
            sts = self.session.client('sts')
            self.caller_identity = sts.get_caller_identity()
            self.user_arn = self.caller_identity['Arn']
            
            if self.config.verbose:
                print(f"✅ Authenticated as: {self.user_arn}")
                print(f"🌐 Gateway: {self.gateway_url}")
        except Exception as e:
            raise Exception(f"Failed to authenticate with AWS: {str(e)}")
    
    def chat(
        self,
        message: str,
        model: str = "sonnet-4.5",
        max_tokens: int = 2000,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        system: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> BedrockResponse:
        """Send a chat message to Claude"""
        
        messages = []
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({
            "role": "user",
            "content": [{"text": message}]
        })
        
        inference_config = {"maxTokens": max_tokens}
        if temperature is not None:
            inference_config["temperature"] = temperature
        if top_p is not None:
            inference_config["topP"] = top_p
        
        model_id = self.config.model_map.get(model, model)
        
        payload = {
            "messages": messages,
            "model": model_id,
            "inferenceConfig": inference_config
        }
        
        if system:
            payload["system"] = [{"text": system}]
        
        return self._send_request(payload, model)
    
    def _send_request(self, payload: Dict[str, Any], model_alias: str) -> BedrockResponse:
        """Internal method to send signed request to gateway"""
        
        request = AWSRequest(
            method='POST',
            url=self.gateway_url,
            data=json.dumps(payload),
            headers={
                'Host': self.host,
                'Content-Type': 'application/json'
            }
        )
        
        SigV4Auth(self.credentials, 'execute-api', self.config.region).add_auth(request)
        
        response = requests.post(
            self.gateway_url,
            headers=dict(request.headers),
            data=json.dumps(payload)
        )
        
        if response.status_code != 200:
            error_detail = response.text
            try:
                error_json = response.json()
                error_detail = error_json.get('error', error_detail)
            except:
                pass
            raise Exception(f"Gateway error ({response.status_code}): {error_detail}")
        
        result = response.json()
        
        if 'body' in result and isinstance(result['body'], str):
            bedrock_response = json.loads(result['body'])
        else:
            bedrock_response = result
        
        text = ""
        if 'output' in bedrock_response and 'message' in bedrock_response['output']:
            message = bedrock_response['output']['message']
            if 'content' in message:
                for content_block in message['content']:
                    if 'text' in content_block:
                        text += content_block['text']
        
        usage = bedrock_response.get('usage', {})
        metrics = bedrock_response.get('metrics', {})
        
        return BedrockResponse(
            text=text,
            tokens=usage.get('totalTokens', 0),
            input_tokens=usage.get('inputTokens', 0),
            output_tokens=usage.get('outputTokens', 0),
            latency_ms=metrics.get('latencyMs', 0),
            request_id=result.get('headers', {}).get('X-Request-ID', 'unknown'),
            model=model_alias,
            stop_reason=bedrock_response.get('stopReason', 'unknown'),
            raw_response=bedrock_response
        )
    
    def get_available_models(self) -> List[str]:
        """Get list of available model aliases"""
        return list(self.config.model_map.keys())


_global_config: Optional[Config] = None


def configure(
    gateway_url: Optional[str] = None,
    api_id: Optional[str] = None,
    region: Optional[str] = None,
    profile: Optional[str] = None,
    model_map: Optional[Dict[str, str]] = None,
    save: bool = False
):
    """Configure global settings for the bedrock_gateway_client"""
    global _global_config
    
    config = Config()
    if gateway_url:
        config.gateway_url = gateway_url
    if api_id:
        config.api_id = api_id
    if region:
        config.region = region
    if profile:
        config.aws_profile = profile
    if model_map:
        config.model_map = model_map
    
    _global_config = config
    
    if save:
        config.save()
        print(f"✅ Configuration saved to ~/.bedrock-gateway/config.yaml")


def chat(message: str, model: str = "sonnet-4.5", **kwargs) -> str:
    """Quick chat function - returns just the text response"""
    client = BedrockClient(config=_global_config)
    response = client.chat(message, model=model, **kwargs)
    return response.text
