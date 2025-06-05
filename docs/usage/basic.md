# Basic Usage

Learn the fundamental concepts and workflows for using LLM as a Judge effectively.

## Core Concepts

### Documents
Documents are the text content you want to evaluate. They can be:
- Essays and academic papers
- Blog posts and articles
- Business reports and proposals
- Creative writing and stories
- Technical documentation

### Rubrics
Rubrics define how documents should be evaluated. They contain:
- **Criteria**: Specific aspects to evaluate (e.g., clarity, evidence, structure)
- **Levels**: Score levels (typically 1-5) with descriptive rules
- **Descriptions**: Clear explanations of what each criterion measures

### Providers
LLM providers are the AI services that perform the evaluation:
- **OpenAI**: GPT-3.5, GPT-4 models
- **Anthropic**: Claude models
- **Custom**: Extensible architecture for other providers

## Basic Workflow

### 1. Prepare Your Content

Ensure your document is in a readable text format:

```bash
# Plain text files work best
echo "Your document content..." > document.txt

# Or use existing files
cp my_essay.md document.txt
```

### 2. Choose or Create a Rubric

Use the provided sample rubric or create your own:

```bash
# Use the sample rubric for general document evaluation
ls tests/rubric.json

# Or create a custom rubric (see Rubric Creation guide)
cp tests/rubric.json my_custom_rubric.json
```

### 3. Run the Evaluation

Execute the evaluation with your chosen parameters:

```bash
python -m src.cli \
  --document document.txt \
  --rubric tests/rubric.json \
  --provider openai
```

### 4. Review Results

Examine the structured output:

```bash
# Results are printed to stdout by default
# Or save to a file for later analysis
python -m src.cli \
  --document document.txt \
  --rubric tests/rubric.json \
  --output results.json
```

## Command Line Interface

### Basic Syntax

```bash
python -m src.cli [OPTIONS] --document DOCUMENT --rubric RUBRIC
```

### Essential Options

| Option | Description | Example |
|--------|-------------|---------|
| `--document` | Path to document file | `--document essay.txt` |
| `--rubric` | Path to rubric JSON file | `--rubric my_rubric.json` |
| `--provider` | LLM provider to use | `--provider openai` |
| `--output` | Save results to file | `--output results.json` |
| `--model` | Specific model name | `--model gpt-4` |
| `--verbose` | Show detailed progress | `--verbose` |

### Examples

#### Basic Evaluation
```bash
python -m src.cli \
  --document my_essay.txt \
  --rubric tests/rubric.json
```

#### With Specific Model
```bash
python -m src.cli \
  --document my_essay.txt \
  --rubric tests/rubric.json \
  --provider openai \
  --model gpt-4
```

#### Multiple Documents
```bash
python -m src.cli \
  --documents essay1.txt essay2.txt essay3.txt \
  --rubric tests/rubric.json \
  --output batch_results.json
```

#### Verbose Output
```bash
python -m src.cli \
  --document my_essay.txt \
  --rubric tests/rubric.json \
  --verbose
```

## Python API

For programmatic use, import and use the evaluation components directly:

### Basic API Usage

```python
from src.evaluator import DocumentEvaluator
from src.criteria import Criteria
from src.llm_providers import OpenAIProvider

# Load your rubric
criteria = Criteria.from_json_file("tests/rubric.json")

# Initialize the LLM provider
provider = OpenAIProvider(model="gpt-3.5-turbo")

# Create evaluator
evaluator = DocumentEvaluator(provider, criteria)

# Load and evaluate document
with open("my_document.txt", "r") as f:
    document_text = f.read()

results = evaluator.evaluate(document_text)

# Access results
print(f"Overall Score: {results.overall_score}")
print(f"Criteria Scores: {results.criteria_scores}")
```

### Advanced API Usage

```python
from src.evaluator import DocumentEvaluator
from src.criteria import Criteria, Criterion, Level
from src.llm_providers import AnthropicProvider

# Create custom criteria programmatically
custom_criterion = Criterion(
    name="creativity",
    description="How creative and original is the content?",
    levels=[
        Level(score=5, rule="Highly creative with unique insights"),
        Level(score=4, rule="Creative with some original ideas"),
        Level(score=3, rule="Moderately creative"),
        Level(score=2, rule="Limited creativity"),
        Level(score=1, rule="Lacks creativity or originality")
    ]
)

criteria = Criteria(criteria=[custom_criterion])

# Use different provider
provider = AnthropicProvider(model="claude-3-sonnet")
evaluator = DocumentEvaluator(provider, criteria)

# Evaluate multiple documents
documents = ["doc1.txt", "doc2.txt", "doc3.txt"]
all_results = []

for doc_path in documents:
    with open(doc_path, "r") as f:
        doc_text = f.read()
    
    result = evaluator.evaluate(doc_text)
    all_results.append({
        "document": doc_path,
        "score": result.overall_score,
        "details": result.criteria_scores
    })

# Analyze results
for result in all_results:
    print(f"{result['document']}: {result['score']:.2f}")
```

## Understanding Results

### Result Structure

Evaluation results contain several components:

```json
{
  "overall_score": 4.2,
  "criteria_scores": {
    "criterion_name": 4,
    "another_criterion": 5
  },
  "detailed_feedback": {
    "criterion_name": "Explanation of the score...",
    "another_criterion": "Another explanation..."
  },
  "metadata": {
    "provider": "openai",
    "model": "gpt-3.5-turbo",
    "timestamp": "2024-01-15T10:30:00Z",
    "rubric_file": "tests/rubric.json",
    "document_length": 1250
  }
}
```

### Score Interpretation

| Score | Meaning | Description |
|-------|---------|-------------|
| 5 | Excellent | Exceeds expectations significantly |
| 4 | Good | Meets expectations well |
| 3 | Satisfactory | Meets basic expectations |
| 2 | Needs Improvement | Below expectations |
| 1 | Poor | Well below expectations |

### Using Feedback

The `detailed_feedback` section provides explanations for each score:

- **Understand Strengths**: High-scoring criteria show what works well
- **Identify Improvements**: Lower scores indicate areas for development  
- **Comparative Analysis**: Compare feedback across multiple documents
- **Rubric Validation**: Ensure feedback aligns with your rubric rules

## Provider-Specific Features

### OpenAI Provider

```python
from src.llm_providers import OpenAIProvider

# Different models available
provider = OpenAIProvider(model="gpt-3.5-turbo")  # Faster, cheaper
provider = OpenAIProvider(model="gpt-4")          # More capable, slower

# Custom parameters
provider = OpenAIProvider(
    model="gpt-3.5-turbo",
    temperature=0.1,  # More deterministic
    max_tokens=2000   # Longer responses
)
```

### Anthropic Provider

```python
from src.llm_providers import AnthropicProvider

# Claude models
provider = AnthropicProvider(model="claude-3-sonnet")
provider = AnthropicProvider(model="claude-3-opus")

# Custom parameters
provider = AnthropicProvider(
    model="claude-3-sonnet",
    temperature=0.0,  # Deterministic
    max_tokens=1500
)
```

## Configuration

### Environment Variables

Set up your environment for consistent behavior:

```bash
# Create .env file
cat > .env << 'EOF'
# OpenAI Configuration
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Anthropic Configuration
ANTHROPIC_API_KEY=your_anthropic_key_here
ANTHROPIC_MODEL=claude-3-sonnet

# Default Settings
DEFAULT_LLM_PROVIDER=openai
DEFAULT_TEMPERATURE=0.1
DEFAULT_MAX_TOKENS=2000
EOF
```

### Using Configuration

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use in your code
provider = OpenAIProvider(
    model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
    temperature=float(os.getenv("DEFAULT_TEMPERATURE", 0.1))
)
```

## Error Handling

### Common Issues

#### API Key Not Found
```bash
# Check environment
echo $OPENAI_API_KEY

# Set if missing
export OPENAI_API_KEY="your-key-here"
```

#### Invalid Rubric Format
```bash
# Validate JSON
python -c "
import json
try:
    with open('my_rubric.json') as f:
        data = json.load(f)
    print('✓ Valid JSON')
    print(f'Criteria count: {len(data.get(\"criteria\", []))}')
except Exception as e:
    print(f'✗ Error: {e}')
"
```

#### Document Reading Issues
```bash
# Check file exists and is readable
test -r my_document.txt && echo "✓ File readable" || echo "✗ File not found/readable"

# Check encoding (should be UTF-8)
file my_document.txt
```

### Programmatic Error Handling

```python
try:
    from src.evaluator import DocumentEvaluator
    from src.criteria import Criteria
    from src.llm_providers import OpenAIProvider
    
    # Load components
    criteria = Criteria.from_json_file("rubric.json")
    provider = OpenAIProvider()
    evaluator = DocumentEvaluator(provider, criteria)
    
    # Evaluate
    with open("document.txt", "r", encoding="utf-8") as f:
        document = f.read()
    
    results = evaluator.evaluate(document)
    
except FileNotFoundError as e:
    print(f"File not found: {e}")
except json.JSONDecodeError as e:
    print(f"Invalid JSON in rubric: {e}")
except Exception as e:
    print(f"Evaluation error: {e}")
```

## Performance Tips

### Optimizing Evaluations

1. **Choose Appropriate Models**: Balance cost and quality
   - GPT-3.5-turbo: Fast and economical for most use cases
   - GPT-4: Higher quality for complex evaluations
   - Claude-3-sonnet: Good balance of speed and capability

2. **Batch Processing**: Evaluate multiple documents efficiently
   ```bash
   python -m src.cli --documents *.txt --rubric rubric.json
   ```

3. **Caching**: Cache results for repeated evaluations
   ```python
   # Save results for later analysis
   import json
   with open("cached_results.json", "w") as f:
       json.dump(results.dict(), f)
   ```

4. **Parallel Processing**: Use multiple providers simultaneously
   ```python
   import asyncio
   from concurrent.futures import ThreadPoolExecutor
   
   # Evaluate with multiple providers in parallel
   def evaluate_with_provider(provider_name):
       # Implementation here
       pass
   
   with ThreadPoolExecutor() as executor:
       futures = [
           executor.submit(evaluate_with_provider, "openai"),
           executor.submit(evaluate_with_provider, "anthropic")
       ]
       results = [f.result() for f in futures]
   ```

## Next Steps

Now that you understand basic usage:

1. **[Create Custom Rubrics](rubrics.md)** - Design evaluation criteria for your needs
2. **[Multiple Providers](providers.md)** - Compare results across different AI models
3. **[CLI Reference](cli.md)** - Master all command-line options
4. **[Advanced Features](../advanced/custom-criteria.md)** - Explore sophisticated evaluation techniques

## Quick Reference

### Common Commands
```bash
# Basic evaluation
python -m src.cli --document doc.txt --rubric rubric.json

# Specify provider and model
python -m src.cli --document doc.txt --rubric rubric.json --provider openai --model gpt-4

# Save results
python -m src.cli --document doc.txt --rubric rubric.json --output results.json

# Multiple documents
python -m src.cli --documents *.txt --rubric rubric.json

# Verbose mode
python -m src.cli --document doc.txt --rubric rubric.json --verbose
```

### Key Files
- **Documents**: Plain text files (.txt, .md)
- **Rubrics**: JSON files with criteria definitions
- **Results**: JSON files with scores and feedback
- **Configuration**: .env files with API keys and settings