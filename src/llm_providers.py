from typing import Optional, Union, Dict, Any
from abc import ABC, abstractmethod
import os
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models import KnownModelName


class LLMConfig(BaseModel):
    """Configuration for LLM providers"""
    model_name: str
    api_key: Optional[str] = None
    temperature: float = Field(default=0.3, ge=0.0, le=2.0)
    max_tokens: Optional[int] = None
    timeout: int = Field(default=60, gt=0)
    
    class Config:
        extra = "allow"  # Allow additional provider-specific parameters


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
    
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Generate a response from the LLM"""
        pass
    
    @abstractmethod
    def generate_sync(self, prompt: str) -> str:
        """Synchronous version of generate"""
        pass


class PydanticAIProvider(LLMProvider):
    """LLM Provider using Pydantic AI framework
    
    Pydantic AI is a Python agent framework that provides type-safe,
    production-ready access to multiple LLM providers.
    """
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        
        # Map model names to Pydantic AI model types
        model_mapping = {
            "gpt-4o": "openai:gpt-4o",
            "gpt-4o-mini": "openai:gpt-4o-mini",
            "gpt-4-turbo": "openai:gpt-4-turbo",
            "gpt-3.5-turbo": "openai:gpt-3.5-turbo",
            "claude-3-5-sonnet-latest": "claude-3-5-sonnet-latest",
            "claude-3-5-haiku-latest": "claude-3-5-haiku-latest",
            "claude-3-opus-latest": "claude-3-opus-latest",
        }
        
        # Get the model name, defaulting to the exact string if not in mapping
        pydantic_model = model_mapping.get(config.model_name, config.model_name)
        
        # Create the agent with model configuration
        self.agent = Agent(
            model=pydantic_model,
            model_settings={
                "temperature": config.temperature,
                "max_tokens": config.max_tokens,
            }
        )
    
    async def generate(self, prompt: str) -> str:
        """Generate a response using Pydantic AI"""
        result = await self.agent.run(prompt)
        # Handle both old and new Pydantic AI API
        return getattr(result, 'output', getattr(result, 'data', ''))
    
    def generate_sync(self, prompt: str) -> str:
        """Synchronous version using run_sync"""
        result = self.agent.run_sync(prompt)
        # Handle both old and new Pydantic AI API
        return getattr(result, 'output', getattr(result, 'data', ''))


class OpenAIProvider(LLMProvider):
    """Direct OpenAI API provider (fallback option)"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        try:
            from openai import OpenAI
            api_key = config.api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key not provided")
            self.client = OpenAI(api_key=api_key, timeout=config.timeout)
        except ImportError:
            raise ImportError("OpenAI package not installed")
    
    async def generate(self, prompt: str) -> str:
        """Async generation - uses sync client for now"""
        return self.generate_sync(prompt)
    
    def generate_sync(self, prompt: str) -> str:
        """Generate using OpenAI API"""
        response = self.client.chat.completions.create(
            model=self.config.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        return response.choices[0].message.content


class AnthropicProvider(LLMProvider):
    """Direct Anthropic API provider (fallback option)"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        try:
            from anthropic import Anthropic
            api_key = config.api_key or os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("Anthropic API key not provided")
            self.client = Anthropic(api_key=api_key, timeout=config.timeout)
        except ImportError:
            raise ImportError("Anthropic package not installed")
    
    async def generate(self, prompt: str) -> str:
        """Async generation - uses sync client for now"""
        return self.generate_sync(prompt)
    
    def generate_sync(self, prompt: str) -> str:
        """Generate using Anthropic API"""
        response = self.client.messages.create(
            model=self.config.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens or 4096
        )
        return response.content[0].text


def create_llm_provider(
    provider_type: str = "pydantic_ai",
    config: Optional[Union[LLMConfig, Dict[str, Any]]] = None
) -> LLMProvider:
    """Factory function to create LLM providers
    
    Args:
        provider_type: Type of provider:
            - "pydantic_ai": Use Pydantic AI framework (recommended)
            - "openai": Direct OpenAI API access
            - "anthropic": Direct Anthropic API access
        config: LLMConfig object or dict with configuration
    
    Returns:
        LLMProvider instance
    """
    if config is None:
        config = LLMConfig(model_name="gpt-4o-mini")
    elif isinstance(config, dict):
        config = LLMConfig(**config)
    
    providers = {
        "pydantic_ai": PydanticAIProvider,
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider
    }
    
    provider_class = providers.get(provider_type.lower())
    if not provider_class:
        raise ValueError(f"Unknown provider type: {provider_type}")
    
    return provider_class(config)