"""Configuration management for Bedrock Gateway Client"""

import os
import yaml
from pathlib import Path
from typing import Optional, Dict
from dataclasses import dataclass, field


@dataclass
class Config:
    """Configuration for Bedrock Gateway Client"""
    
    gateway_url: Optional[str] = None
    api_id: Optional[str] = None
    region: str = "us-east-1"
    stage: str = "prod"
    path: str = "/invoke"
    aws_profile: Optional[str] = None
    model_map: Dict[str, str] = field(default_factory=lambda: {
        'sonnet-4.5': 'anthropic.claude-sonnet-4-5-v1:0',
        'sonnet': 'anthropic.claude-sonnet-4-5-v1:0',
        'haiku-4.5': 'anthropic.claude-haiku-4-5-v1:0',
        'haiku': 'anthropic.claude-haiku-4-5-v1:0',
    })
    verbose: bool = False
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Load configuration from environment variables"""
        return cls(
            gateway_url=os.getenv('BEDROCK_GATEWAY_URL'),
            api_id=os.getenv('BEDROCK_GATEWAY_API_ID'),
            region=os.getenv('BEDROCK_GATEWAY_REGION', 'us-east-1'),
            stage=os.getenv('BEDROCK_GATEWAY_STAGE', 'prod'),
            path=os.getenv('BEDROCK_GATEWAY_PATH', '/invoke'),
            aws_profile=os.getenv('AWS_PROFILE'),
            verbose=os.getenv('BEDROCK_GATEWAY_VERBOSE', '').lower() == 'true'
        )
    
    @classmethod
    def from_file(cls, path: Optional[str] = None) -> 'Config':
        """Load configuration from YAML file"""
        if path is None:
            path = os.path.expanduser('~/.bedrock-gateway/config.yaml')
        
        config_path = Path(path)
        if not config_path.exists():
            return cls()
        
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f) or {}
        
        return cls(**data)
    
    def save(self, path: Optional[str] = None):
        """Save configuration to YAML file"""
        if path is None:
            path = os.path.expanduser('~/.bedrock-gateway/config.yaml')
        
        config_path = Path(path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'gateway_url': self.gateway_url,
            'api_id': self.api_id,
            'region': self.region,
            'stage': self.stage,
            'path': self.path,
            'aws_profile': self.aws_profile,
            'model_map': self.model_map,
            'verbose': self.verbose
        }
        
        with open(config_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
    
    def get_full_url(self) -> str:
        """Get the full gateway URL"""
        if self.gateway_url:
            return self.gateway_url
        
        if not self.api_id:
            raise ValueError(
                "Either gateway_url or api_id must be configured.\n"
                "Set via environment variable BEDROCK_GATEWAY_URL or BEDROCK_GATEWAY_API_ID"
            )
        
        return f"https://{self.api_id}.execute-api.{self.region}.amazonaws.com/{self.stage}{self.path}"
    
    def get_host(self) -> str:
        """Get the host header for signing"""
        if self.api_id:
            return f"{self.api_id}.execute-api.{self.region}.amazonaws.com"
        
        from urllib.parse import urlparse
        parsed = urlparse(self.gateway_url)
        return parsed.netloc
