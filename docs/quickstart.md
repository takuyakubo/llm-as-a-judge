# Quick Start

Get up and running with LLM as a Judge in under 30 minutes! This guide will walk you through your first document evaluation.

## Prerequisites

- LLM as a Judge installed ([Installation Guide](installation.md))
- At least one LLM provider API key configured
- Python virtual environment activated

## Your First Evaluation

### Step 1: Prepare a Document

Create a sample document to evaluate:

```bash
cat > sample_document.txt << 'EOF'
Climate change represents one of the most pressing challenges of our time. The scientific consensus is clear: human activities, particularly the burning of fossil fuels, are the primary drivers of recent climate change.

The evidence is overwhelming. Global temperatures have risen by approximately 1.1°C since the late 19th century. Arctic sea ice is declining, sea levels are rising, and extreme weather events are becoming more frequent and severe.

However, there is reason for hope. Renewable energy technologies have become increasingly cost-competitive. Solar and wind power are now the cheapest sources of electricity in many regions. Countries and corporations worldwide are committing to net-zero emissions targets.

The transition to a sustainable future requires immediate action. We must accelerate the deployment of clean energy, improve energy efficiency, and develop carbon capture technologies. Individual actions, while important, must be coupled with systemic changes in policy and infrastructure.
EOF
```

### Step 2: Run Your First Evaluation

Use the provided sample rubric to evaluate your document:

```bash
python -m src.cli \
  --document sample_document.txt \
  --rubric tests/rubric.json \
  --provider openai \
  --output results.json
```

### Step 3: View Results

Check the evaluation results:

```bash
cat results.json
```

You should see structured scores for each criterion:

```json
{
  "overall_score": 4.2,
  "criteria_scores": {
    "claim_clarity": 5,
    "coherence": 4,
    "evidence_quality": 4,
    "depth_of_reasoning": 4,
    "readability": 5
  },
  "detailed_feedback": {
    "claim_clarity": "The main argument about climate change is clearly stated...",
    "coherence": "The document flows logically from problem to solution...",
    ...
  }
}
```

## Understanding the Rubric

Let's examine the evaluation criteria used in `tests/rubric.json`:

### Criterion Example: Claim Clarity

```json
{
  "name": "claim_clarity",
  "description": "主張の明確さ",
  "levels": [
    {
      "score": 5,
      "rule": "主要な主張が冒頭で明確に提示され、一貫して維持されている"
    },
    {
      "score": 4,
      "rule": "主要な主張が明確だが、一部で曖昧さがある"
    },
    {
      "score": 3,
      "rule": "主張は識別できるが、不明確な部分がある"
    },
    {
      "score": 2,
      "rule": "主張が曖昧で、複数の解釈が可能"
    },
    {
      "score": 1,
      "rule": "主張が不明確または矛盾している"
    }
  ]
}
```

## Customizing Your Evaluation

### Use Different Providers

Try different LLM providers to compare results:

```bash
# Using Anthropic Claude
python -m src.cli \
  --document sample_document.txt \
  --rubric tests/rubric.json \
  --provider anthropic

# Using OpenAI with specific model
python -m src.cli \
  --document sample_document.txt \
  --rubric tests/rubric.json \
  --provider openai \
  --model gpt-4
```

### Create a Custom Rubric

Create your own evaluation criteria:

```bash
cat > my_rubric.json << 'EOF'
{
  "criteria": [
    {
      "name": "persuasiveness",
      "description": "How convincing is the argument?",
      "levels": [
        {
          "score": 5,
          "rule": "Extremely persuasive with compelling evidence and logic"
        },
        {
          "score": 4,
          "rule": "Very persuasive with good supporting evidence"
        },
        {
          "score": 3,
          "rule": "Moderately persuasive with some evidence"
        },
        {
          "score": 2,
          "rule": "Somewhat persuasive but lacks strong evidence"
        },
        {
          "score": 1,
          "rule": "Not persuasive with weak or no evidence"
        }
      ]
    }
  ]
}
EOF
```

Use your custom rubric:

```bash
python -m src.cli \
  --document sample_document.txt \
  --rubric my_rubric.json
```

## Batch Evaluation

Evaluate multiple documents at once:

```bash
# Create multiple sample documents
echo "Document 1 content..." > doc1.txt
echo "Document 2 content..." > doc2.txt
echo "Document 3 content..." > doc3.txt

# Evaluate all documents
python -m src.cli \
  --documents doc1.txt doc2.txt doc3.txt \
  --rubric tests/rubric.json \
  --output batch_results.json
```

## Python API Usage

You can also use the framework programmatically:

```python
from src.evaluator import DocumentEvaluator
from src.criteria import Criteria
from src.llm_providers import OpenAIProvider

# Load criteria
criteria = Criteria.from_json_file("tests/rubric.json")

# Initialize evaluator
provider = OpenAIProvider()
evaluator = DocumentEvaluator(provider, criteria)

# Evaluate document
with open("sample_document.txt", "r") as f:
    document = f.read()

results = evaluator.evaluate(document)
print(f"Overall score: {results.overall_score}")
```

## Understanding Results

### Score Interpretation

- **5**: Excellent - Exceeds expectations
- **4**: Good - Meets expectations well
- **3**: Satisfactory - Meets basic expectations
- **2**: Needs Improvement - Below expectations
- **1**: Poor - Well below expectations

### Result Components

- **overall_score**: Average of all criteria scores
- **criteria_scores**: Individual scores for each criterion
- **detailed_feedback**: Explanatory text for each score
- **metadata**: Evaluation details (model used, timestamp, etc.)

## Next Steps

Now that you've completed your first evaluation:

1. **Learn More**: Read the [Basic Usage Guide](usage/basic.md)
2. **Create Custom Rubrics**: Check out [Rubric Creation](usage/rubrics.md)
3. **Explore Providers**: Learn about [Multiple Providers](usage/providers.md)
4. **Advanced Features**: Dive into [Advanced Usage](advanced/custom-criteria.md)

## Common Issues

### API Key Not Found

```bash
# Error: OpenAI API key not found
# Solution: Check your .env file
echo $OPENAI_API_KEY  # Should not be empty
```

### Module Import Error

```bash
# Error: No module named 'src'
# Solution: Run from project root directory
cd /path/to/llm-as-a-judge
python -m src.cli --help
```

### JSON Format Error

```bash
# Error: Invalid JSON in rubric file
# Solution: Validate your JSON
python -c "import json; json.load(open('my_rubric.json'))"
```

For more troubleshooting help, see our [Troubleshooting Guide](troubleshooting.md).