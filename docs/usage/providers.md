# Multiple LLM Providers

Learn how to work with different AI providers to get the best evaluation results for your use cases.

## Supported Providers

LLM as a Judge supports multiple AI providers, each with their own strengths and characteristics:

### OpenAI
- **Models**: GPT-3.5 Turbo, GPT-4, GPT-4 Turbo
- **Strengths**: Fast, cost-effective, widely compatible
- **Best for**: General document evaluation, high-volume processing

### Anthropic
- **Models**: Claude-3 Haiku, Claude-3 Sonnet, Claude-3 Opus
- **Strengths**: Nuanced understanding, detailed analysis
- **Best for**: Complex documents, detailed feedback requirements

## Quick Provider Comparison

| Provider | Speed | Cost | Quality | Best Use Case |
|----------|-------|------|---------|---------------|
| OpenAI GPT-3.5 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | High-volume, basic evaluation |
| OpenAI GPT-4 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | Complex documents, detailed analysis |
| Claude-3 Sonnet | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | Balanced speed and quality |
| Claude-3 Opus | ⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | Highest quality analysis |

## Setting Up Providers

### OpenAI Setup

1. **Get API Key**
   ```bash
   # Visit: https://platform.openai.com/api-keys
   # Create new secret key
   ```

2. **Configure Environment**
   ```bash
   # Add to .env file
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-3.5-turbo  # Optional default
   ```

3. **Test Connection**
   ```bash
   python -c "
   from src.llm_providers import OpenAIProvider
   provider = OpenAIProvider()
   print('✓ OpenAI connected successfully')
   "
   ```

### Anthropic Setup

1. **Get API Key**
   ```bash
   # Visit: https://console.anthropic.com/
   # Navigate to API Keys section
   ```

2. **Configure Environment**
   ```bash
   # Add to .env file
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ANTHROPIC_MODEL=claude-3-sonnet-20240229  # Optional default
   ```

3. **Test Connection**
   ```bash
   python -c "
   from src.llm_providers import AnthropicProvider
   provider = AnthropicProvider()
   print('✓ Anthropic connected successfully')
   "
   ```

## Using Different Providers

### Command Line Usage

#### Specify Provider
```bash
# Use OpenAI (default)
python -m src.cli --document essay.txt --rubric rubric.json --provider openai

# Use Anthropic
python -m src.cli --document essay.txt --rubric rubric.json --provider anthropic
```

#### Specify Model
```bash
# OpenAI with specific model
python -m src.cli \
  --document essay.txt \
  --rubric rubric.json \
  --provider openai \
  --model gpt-4

# Anthropic with specific model
python -m src.cli \
  --document essay.txt \
  --rubric rubric.json \
  --provider anthropic \
  --model claude-3-opus-20240229
```

### Python API Usage

#### Basic Provider Usage
```python
from src.evaluator import DocumentEvaluator
from src.criteria import Criteria
from src.llm_providers import OpenAIProvider, AnthropicProvider

# Load criteria
criteria = Criteria.from_json_file("rubric.json")

# OpenAI evaluation
openai_provider = OpenAIProvider(model="gpt-4")
openai_evaluator = DocumentEvaluator(openai_provider, criteria)

# Anthropic evaluation
anthropic_provider = AnthropicProvider(model="claude-3-sonnet-20240229")
anthropic_evaluator = DocumentEvaluator(anthropic_provider, criteria)

# Evaluate same document with both providers
with open("document.txt", "r") as f:
    document = f.read()

openai_results = openai_evaluator.evaluate(document)
anthropic_results = anthropic_evaluator.evaluate(document)

print(f"OpenAI Score: {openai_results.overall_score}")
print(f"Anthropic Score: {anthropic_results.overall_score}")
```

#### Advanced Provider Configuration
```python
from src.llm_providers import OpenAIProvider, AnthropicProvider

# OpenAI with custom parameters
openai_provider = OpenAIProvider(
    model="gpt-4",
    temperature=0.1,    # More deterministic
    max_tokens=2000,    # Longer responses
    timeout=30          # 30 second timeout
)

# Anthropic with custom parameters
anthropic_provider = AnthropicProvider(
    model="claude-3-opus-20240229",
    temperature=0.0,    # Deterministic
    max_tokens=1500,
    timeout=60
)
```

## Comparing Provider Results

### Side-by-Side Comparison

```bash
# Create comparison script
cat > compare_providers.py << 'EOF'
import json
from src.evaluator import DocumentEvaluator
from src.criteria import Criteria
from src.llm_providers import OpenAIProvider, AnthropicProvider

def compare_providers(document_path, rubric_path):
    # Load document and criteria
    with open(document_path, 'r') as f:
        document = f.read()
    criteria = Criteria.from_json_file(rubric_path)
    
    # Evaluate with both providers
    providers = {
        "OpenAI GPT-4": OpenAIProvider(model="gpt-4"),
        "Claude-3 Sonnet": AnthropicProvider(model="claude-3-sonnet-20240229")
    }
    
    results = {}
    for name, provider in providers.items():
        evaluator = DocumentEvaluator(provider, criteria)
        result = evaluator.evaluate(document)
        results[name] = result
    
    # Compare results
    print("Provider Comparison Results")
    print("=" * 50)
    for provider_name, result in results.items():
        print(f"{provider_name}: {result.overall_score:.2f}")
        for criterion, score in result.criteria_scores.items():
            print(f"  {criterion}: {score}")
        print()
    
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python compare_providers.py <document> <rubric>")
        sys.exit(1)
    
    compare_providers(sys.argv[1], sys.argv[2])
EOF

# Run comparison
python compare_providers.py document.txt rubric.json
```

### Batch Comparison

```bash
# Compare multiple documents across providers
cat > batch_compare.py << 'EOF'
import json
import os
from src.evaluator import DocumentEvaluator
from src.criteria import Criteria
from src.llm_providers import OpenAIProvider, AnthropicProvider

def batch_compare(document_dir, rubric_path, output_file):
    criteria = Criteria.from_json_file(rubric_path)
    
    providers = {
        "gpt-4": OpenAIProvider(model="gpt-4"),
        "claude-3-sonnet": AnthropicProvider(model="claude-3-sonnet-20240229")
    }
    
    results = []
    
    for filename in os.listdir(document_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(document_dir, filename)
            with open(filepath, 'r') as f:
                document = f.read()
            
            doc_results = {"document": filename}
            
            for provider_name, provider in providers.items():
                evaluator = DocumentEvaluator(provider, criteria)
                result = evaluator.evaluate(document)
                doc_results[provider_name] = {
                    "overall_score": result.overall_score,
                    "criteria_scores": result.criteria_scores
                }
            
            results.append(doc_results)
            print(f"Completed: {filename}")
    
    # Save results
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python batch_compare.py <document_dir> <rubric> <output>")
        sys.exit(1)
    
    batch_compare(sys.argv[1], sys.argv[2], sys.argv[3])
EOF

# Run batch comparison
python batch_compare.py documents/ rubric.json comparison_results.json
```

## Provider-Specific Features

### OpenAI Features

#### Model Selection
```python
from src.llm_providers import OpenAIProvider

# Fast and economical
provider = OpenAIProvider(model="gpt-3.5-turbo")

# Balanced performance
provider = OpenAIProvider(model="gpt-4")

# Latest capabilities
provider = OpenAIProvider(model="gpt-4-turbo-preview")
```

#### Token Management
```python
# Optimize for token usage
provider = OpenAIProvider(
    model="gpt-3.5-turbo",
    max_tokens=1000,        # Limit response length
    temperature=0.1         # Reduce verbosity
)
```

#### Batch Processing Optimization
```python
# For high-volume processing
import asyncio
from concurrent.futures import ThreadPoolExecutor

def evaluate_batch_openai(documents, rubric_path):
    criteria = Criteria.from_json_file(rubric_path)
    provider = OpenAIProvider(model="gpt-3.5-turbo")
    
    def evaluate_single(doc):
        evaluator = DocumentEvaluator(provider, criteria)
        return evaluator.evaluate(doc)
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(evaluate_single, documents))
    
    return results
```

### Anthropic Features

#### Model Selection
```python
from src.llm_providers import AnthropicProvider

# Fast and efficient
provider = AnthropicProvider(model="claude-3-haiku-20240307")

# Balanced performance
provider = AnthropicProvider(model="claude-3-sonnet-20240229")

# Highest quality
provider = AnthropicProvider(model="claude-3-opus-20240229")
```

#### Long Document Handling
```python
# Optimized for long documents
provider = AnthropicProvider(
    model="claude-3-sonnet-20240229",
    max_tokens=4000,        # Longer responses
    temperature=0.0         # Consistent analysis
)
```

#### Detailed Analysis
```python
# For comprehensive feedback
provider = AnthropicProvider(
    model="claude-3-opus-20240229",
    temperature=0.1,
    max_tokens=3000
)
```

## Choosing the Right Provider

### Decision Matrix

| Use Case | Recommended Provider | Model | Reasoning |
|----------|---------------------|-------|-----------|
| High-volume basic evaluation | OpenAI | gpt-3.5-turbo | Fast, cost-effective |
| Academic paper assessment | Anthropic | claude-3-sonnet | Nuanced understanding |
| Creative writing evaluation | Anthropic | claude-3-opus | Detailed literary analysis |
| Business document review | OpenAI | gpt-4 | Professional, structured |
| Technical documentation | OpenAI | gpt-4 | Technical accuracy |
| Quick prototyping | OpenAI | gpt-3.5-turbo | Fast iteration |

### Cost Considerations

#### OpenAI Pricing (approximate)
- **GPT-3.5 Turbo**: $0.0010 / 1K input tokens, $0.0020 / 1K output tokens
- **GPT-4**: $0.03 / 1K input tokens, $0.06 / 1K output tokens
- **GPT-4 Turbo**: $0.01 / 1K input tokens, $0.03 / 1K output tokens

#### Anthropic Pricing (approximate)
- **Claude-3 Haiku**: $0.00025 / 1K input tokens, $0.00125 / 1K output tokens
- **Claude-3 Sonnet**: $0.003 / 1K input tokens, $0.015 / 1K output tokens
- **Claude-3 Opus**: $0.015 / 1K input tokens, $0.075 / 1K output tokens

#### Cost Estimation Tool
```python
def estimate_cost(document_length, rubric_criteria_count, provider="openai", model="gpt-3.5-turbo"):
    # Rough token estimation
    input_tokens = document_length // 4 + rubric_criteria_count * 100  # Approximate
    output_tokens = rubric_criteria_count * 200  # Estimated feedback length
    
    pricing = {
        "openai": {
            "gpt-3.5-turbo": {"input": 0.0010, "output": 0.0020},
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03}
        },
        "anthropic": {
            "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
            "claude-3-sonnet": {"input": 0.003, "output": 0.015},
            "claude-3-opus": {"input": 0.015, "output": 0.075}
        }
    }
    
    rates = pricing[provider][model]
    cost = (input_tokens / 1000 * rates["input"]) + (output_tokens / 1000 * rates["output"])
    
    return {
        "estimated_cost": round(cost, 4),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens
    }

# Example usage
print(estimate_cost(5000, 5, "openai", "gpt-3.5-turbo"))
print(estimate_cost(5000, 5, "anthropic", "claude-3-sonnet"))
```

## Best Practices

### Provider Selection Strategy

1. **Start with GPT-3.5 Turbo** for initial testing and prototyping
2. **Upgrade to GPT-4** for production academic or professional use
3. **Use Claude-3 Sonnet** when you need nuanced understanding
4. **Reserve Claude-3 Opus** for the most demanding evaluations

### Quality Assurance

#### Cross-Provider Validation
```python
def validate_rubric_across_providers(document, rubric_path):
    """Test rubric consistency across different providers"""
    criteria = Criteria.from_json_file(rubric_path)
    
    providers = [
        ("OpenAI GPT-4", OpenAIProvider(model="gpt-4")),
        ("Claude-3 Sonnet", AnthropicProvider(model="claude-3-sonnet-20240229"))
    ]
    
    results = []
    for name, provider in providers:
        evaluator = DocumentEvaluator(provider, criteria)
        result = evaluator.evaluate(document)
        results.append((name, result.overall_score, result.criteria_scores))
    
    # Check for consistency
    scores = [r[1] for r in results]
    score_range = max(scores) - min(scores)
    
    print(f"Score range across providers: {score_range:.2f}")
    if score_range > 1.0:
        print("⚠️  High variance detected - consider refining rubric")
    else:
        print("✅ Good consistency across providers")
    
    return results
```

#### A/B Testing Framework
```python
def ab_test_providers(documents, rubric_path, provider_a, provider_b):
    """Compare two providers across multiple documents"""
    criteria = Criteria.from_json_file(rubric_path)
    
    evaluator_a = DocumentEvaluator(provider_a, criteria)
    evaluator_b = DocumentEvaluator(provider_b, criteria)
    
    results = []
    for doc in documents:
        result_a = evaluator_a.evaluate(doc)
        result_b = evaluator_b.evaluate(doc)
        
        results.append({
            "document": doc[:50] + "...",  # Preview
            "provider_a_score": result_a.overall_score,
            "provider_b_score": result_b.overall_score,
            "difference": abs(result_a.overall_score - result_b.overall_score)
        })
    
    # Analyze results
    avg_difference = sum(r["difference"] for r in results) / len(results)
    print(f"Average score difference: {avg_difference:.2f}")
    
    return results
```

### Performance Optimization

#### Caching Strategy
```python
import hashlib
import json
import os

class CachedEvaluator:
    def __init__(self, provider, criteria, cache_dir="evaluation_cache"):
        self.evaluator = DocumentEvaluator(provider, criteria)
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def evaluate(self, document):
        # Create cache key
        content_hash = hashlib.md5(document.encode()).hexdigest()
        cache_file = os.path.join(self.cache_dir, f"{content_hash}.json")
        
        # Check cache
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)
        
        # Evaluate and cache
        result = self.evaluator.evaluate(document)
        with open(cache_file, 'w') as f:
            json.dump(result.dict(), f)
        
        return result
```

#### Rate Limiting
```python
import time
from functools import wraps

def rate_limit(calls_per_minute=60):
    """Decorator to rate limit API calls"""
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Apply to evaluation function
@rate_limit(calls_per_minute=30)
def rate_limited_evaluate(evaluator, document):
    return evaluator.evaluate(document)
```

## Troubleshooting

### Common Issues

#### API Key Errors
```bash
# Check environment variables
echo "OpenAI Key: ${OPENAI_API_KEY:0:10}..."
echo "Anthropic Key: ${ANTHROPIC_API_KEY:0:10}..."

# Test API connectivity
python -c "
from src.llm_providers import OpenAIProvider
try:
    provider = OpenAIProvider()
    print('✅ OpenAI connection successful')
except Exception as e:
    print(f'❌ OpenAI error: {e}')
"
```

#### Rate Limiting
```python
# Handle rate limits gracefully
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def robust_evaluate(evaluator, document):
    try:
        return evaluator.evaluate(document)
    except Exception as e:
        if "rate_limit" in str(e).lower():
            print("Rate limit hit, retrying...")
            raise
        else:
            print(f"Evaluation error: {e}")
            return None
```

#### Model Availability
```python
def check_model_availability():
    """Check which models are available for each provider"""
    
    # OpenAI models
    try:
        from openai import OpenAI
        client = OpenAI()
        models = client.models.list()
        openai_models = [m.id for m in models.data if 'gpt' in m.id]
        print(f"OpenAI models: {openai_models}")
    except Exception as e:
        print(f"OpenAI check failed: {e}")
    
    # Anthropic models (static list)
    anthropic_models = [
        "claude-3-haiku-20240307",
        "claude-3-sonnet-20240229", 
        "claude-3-opus-20240229"
    ]
    print(f"Anthropic models: {anthropic_models}")

check_model_availability()
```

## Next Steps

After mastering multiple providers:

1. **[CLI Reference](cli.md)** - Learn advanced command-line options for provider management
2. **[Custom Criteria](../advanced/custom-criteria.md)** - Create sophisticated evaluation frameworks
3. **[Batch Processing](../advanced/batch.md)** - Scale your evaluations across providers
4. **[Integration Guide](../advanced/integration.md)** - Embed multi-provider evaluation in your workflows

## Quick Reference

### Provider Commands

```bash
# OpenAI with different models
python -m src.cli --document doc.txt --rubric rubric.json --provider openai --model gpt-3.5-turbo
python -m src.cli --document doc.txt --rubric rubric.json --provider openai --model gpt-4

# Anthropic with different models  
python -m src.cli --document doc.txt --rubric rubric.json --provider anthropic --model claude-3-haiku-20240307
python -m src.cli --document doc.txt --rubric rubric.json --provider anthropic --model claude-3-sonnet-20240229
python -m src.cli --document doc.txt --rubric rubric.json --provider anthropic --model claude-3-opus-20240229

# Compare providers
python -m src.cli --document doc.txt --rubric rubric.json --provider openai --output openai_result.json
python -m src.cli --document doc.txt --rubric rubric.json --provider anthropic --output anthropic_result.json
```

### Environment Setup
```bash
# .env file
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
DEFAULT_LLM_PROVIDER=openai
OPENAI_MODEL=gpt-3.5-turbo
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```