# AUTOGENERATED! DO NOT EDIT! File to edit: ../01_dynamodb.ipynb.

# %% auto 0
__all__ = ['TEN_MINUTES_IN_MS', 'Config', 'DynamoDB']

# %% ../01_dynamodb.ipynb 4
from dataclasses import dataclass
from pathlib import Path

import boto3
import rtime.core as rtime

# %% ../01_dynamodb.ipynb 5
TEN_MINUTES_IN_MS = 1000 * 60 * 10

# %% ../01_dynamodb.ipynb 6
@dataclass
class Config:
    """Configuration for a dynamodb instance."""
    region: str
    aki: str | Path
    sak: str | Path


# %% ../01_dynamodb.ipynb 7
class DynamoDB:
    """Wrapper around dynamodb resource."""
    
    def __init__(self, config: Config):
        self.timestamp = 0
        self.resource = self._init_resource()
        self.config = config

    def _init_resource(self):
        """Return the main table."""
        config = self.config
        with open(config.aki, "r") as infile:
            aki = infile.read().strip()
        with open(config.sak, "r") as infile:
            sak = infile.read().strip()
    
        self.timestamp = rtime.timestamp()
        return boto3.resource(
            "dynamodb",
            region_name=config.region,
            aws_access_key_id=aki,
            aws_secret_access_key=sak,
        )
        
    def __getattr__(self, name):
        """Forward requests to the underlying resource."""
        if rtime.timestamp() - self.timestamp > TEN_MINUTES_IN_MS:
            self.resource = self._init_resource()
        return getattr(self.resource, name)
