import unittest
from unittest.mock import Mock, patch, AsyncMock
import asyncio
from src.llm_providers import (
    LLMConfig, 
    PydanticAIProvider, 
    OpenAIProvider, 
    AnthropicProvider,
    create_llm_provider
)


class TestLLMConfig(unittest.TestCase):
    def test_default_values(self):
        config = LLMConfig(model_name="gpt-4o")
        self.assertEqual(config.model_name, "gpt-4o")
        self.assertEqual(config.temperature, 0.3)
        self.assertEqual(config.timeout, 60)
        self.assertIsNone(config.api_key)
        self.assertIsNone(config.max_tokens)
    
    def test_custom_values(self):
        config = LLMConfig(
            model_name="claude-3-opus",
            api_key="test_key",
            temperature=0.7,
            max_tokens=1000,
            timeout=30
        )
        self.assertEqual(config.temperature, 0.7)
        self.assertEqual(config.max_tokens, 1000)
        self.assertEqual(config.timeout, 30)


class TestPydanticAIProvider(unittest.TestCase):
    @patch('src.llm_providers.Agent')
    def test_initialization(self, mock_agent_class):
        config = LLMConfig(model_name="gpt-4o", temperature=0.5)
        provider = PydanticAIProvider(config)
        
        mock_agent_class.assert_called_once_with(
            model="openai:gpt-4o",
            model_settings={
                "temperature": 0.5,
                "max_tokens": None
            }
        )
    
    @patch('src.llm_providers.Agent')
    def test_generate_sync(self, mock_agent_class):
        # Setup mock
        mock_agent = Mock()
        mock_result = Mock()
        mock_result.output = "Test response"
        mock_result.data = "Test response"  # Fallback for old API
        mock_agent.run_sync.return_value = mock_result
        mock_agent_class.return_value = mock_agent
        
        config = LLMConfig(model_name="gpt-4o-mini")
        provider = PydanticAIProvider(config)
        
        response = provider.generate_sync("Test prompt")
        
        mock_agent.run_sync.assert_called_once_with("Test prompt")
        self.assertEqual(response, "Test response")
    
    @patch('src.llm_providers.Agent')
    async def test_generate_async(self, mock_agent_class):
        # Setup mock
        mock_agent = Mock()
        mock_result = Mock()
        mock_result.output = "Test async response"
        mock_result.data = "Test async response"  # Fallback for old API
        
        # Create async mock for run method
        async def mock_run(prompt):
            return mock_result
        
        mock_agent.run = mock_run
        mock_agent_class.return_value = mock_agent
        
        config = LLMConfig(model_name="claude-3-5-sonnet-latest")
        provider = PydanticAIProvider(config)
        
        response = await provider.generate("Test async prompt")
        
        self.assertEqual(response, "Test async response")


class TestOpenAIProvider(unittest.TestCase):
    @patch('openai.OpenAI')
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key'})
    def test_initialization_with_env_key(self, mock_openai_class):
        config = LLMConfig(model_name="gpt-4o")
        provider = OpenAIProvider(config)
        
        mock_openai_class.assert_called_once_with(
            api_key='test_key',
            timeout=60
        )
    
    @patch('openai.OpenAI')
    def test_initialization_with_config_key(self, mock_openai_class):
        config = LLMConfig(model_name="gpt-4o", api_key="config_key")
        provider = OpenAIProvider(config)
        
        mock_openai_class.assert_called_once_with(
            api_key='config_key',
            timeout=60
        )
    
    @patch('openai.OpenAI')
    def test_generate_sync(self, mock_openai_class):
        # Setup mock
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="OpenAI response"))]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client
        
        config = LLMConfig(model_name="gpt-3.5-turbo", api_key="test")
        provider = OpenAIProvider(config)
        
        response = provider.generate_sync("Test prompt")
        
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Test prompt"}],
            temperature=0.3,
            max_tokens=None
        )
        self.assertEqual(response, "OpenAI response")


class TestAnthropicProvider(unittest.TestCase):
    @patch('anthropic.Anthropic')
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test_key'})
    def test_initialization_with_env_key(self, mock_anthropic_class):
        config = LLMConfig(model_name="claude-3-opus")
        provider = AnthropicProvider(config)
        
        mock_anthropic_class.assert_called_once_with(
            api_key='test_key',
            timeout=60
        )
    
    @patch('anthropic.Anthropic')
    def test_generate_sync(self, mock_anthropic_class):
        # Setup mock
        mock_client = Mock()
        mock_content = Mock(text="Anthropic response")
        mock_response = Mock(content=[mock_content])
        mock_client.messages.create.return_value = mock_response
        mock_anthropic_class.return_value = mock_client
        
        config = LLMConfig(model_name="claude-3-opus", api_key="test")
        provider = AnthropicProvider(config)
        
        response = provider.generate_sync("Test prompt")
        
        mock_client.messages.create.assert_called_once_with(
            model="claude-3-opus",
            messages=[{"role": "user", "content": "Test prompt"}],
            temperature=0.3,
            max_tokens=4096
        )
        self.assertEqual(response, "Anthropic response")


class TestCreateLLMProvider(unittest.TestCase):
    def test_create_pydantic_ai_provider(self):
        with patch('src.llm_providers.Agent'):
            provider = create_llm_provider("pydantic_ai", {"model_name": "gpt-4o"})
            self.assertIsInstance(provider, PydanticAIProvider)
    
    def test_create_openai_provider(self):
        with patch('openai.OpenAI'):
            provider = create_llm_provider("openai", {"model_name": "gpt-4o", "api_key": "test"})
            self.assertIsInstance(provider, OpenAIProvider)
    
    def test_create_anthropic_provider(self):
        with patch('anthropic.Anthropic'):
            provider = create_llm_provider("anthropic", {"model_name": "claude-3", "api_key": "test"})
            self.assertIsInstance(provider, AnthropicProvider)
    
    def test_invalid_provider_type(self):
        with self.assertRaises(ValueError) as context:
            create_llm_provider("invalid_provider")
        self.assertIn("Unknown provider type", str(context.exception))
    
    def test_default_config(self):
        with patch('src.llm_providers.Agent'):
            provider = create_llm_provider("pydantic_ai")
            self.assertEqual(provider.config.model_name, "gpt-4o-mini")


if __name__ == '__main__':
    unittest.main()