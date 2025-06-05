# CLI Reference

Complete guide to using the LLM as a Judge command-line interface.

## Overview

The CLI provides three main commands for document evaluation:
- `evaluate` - Evaluate documents using rubrics
- `export` - Export rubrics to XML format
- `show` - Display rubric content in readable format

## Basic Syntax

```bash
python -m src.cli [COMMAND] [OPTIONS] [ARGUMENTS]
```

## Commands

### evaluate

Evaluate a document using a specified rubric.

#### Basic Usage

```bash
# Evaluate a file
python -m src.cli evaluate rubric.json -f document.txt

# Evaluate from stdin
echo "Document content..." | python -m src.cli evaluate rubric.json

# Evaluate with specific provider
python -m src.cli evaluate rubric.json -f document.txt --provider openai
```

#### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `rubric` | Yes | Path to rubric JSON file |

#### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--file` | `-f` | string | stdin | Document file to evaluate |
| `--output-format` | `-o` | choice | pretty | Output format: pretty, json |
| `--mock` | `-m` | flag | false | Use mock evaluation (testing) |
| `--verbose` | `-v` | flag | false | Show detailed reasoning |
| `--provider` | | choice | pydantic_ai | LLM provider: pydantic_ai, openai, anthropic |
| `--model` | | string | auto | Specific model name |
| `--temperature` | | float | 0.3 | Generation temperature |
| `--max-tokens` | | int | auto | Maximum response tokens |

#### Examples

**Basic Evaluation**
```bash
python -m src.cli evaluate tests/rubric.json -f essay.txt
```

**JSON Output**
```bash
python -m src.cli evaluate tests/rubric.json -f essay.txt -o json
```

**Verbose Mode**
```bash
python -m src.cli evaluate tests/rubric.json -f essay.txt -v
```

**Specific Provider and Model**
```bash
python -m src.cli evaluate tests/rubric.json -f essay.txt \
  --provider openai --model gpt-4
```

**From Stdin**
```bash
cat essay.txt | python -m src.cli evaluate tests/rubric.json
```

**Mock Mode (Testing)**
```bash
python -m src.cli evaluate tests/rubric.json -f essay.txt --mock
```

### export

Export rubric criteria to XML format for inspection or integration.

#### Basic Usage

```bash
# Export to stdout
python -m src.cli export rubric.json

# Export to file
python -m src.cli export rubric.json -o criteria.xml
```

#### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `rubric` | Yes | Path to rubric JSON file |

#### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--output` | `-o` | string | stdout | Output file path |

#### Examples

**Export to File**
```bash
python -m src.cli export tests/rubric.json -o my_criteria.xml
```

**View XML Structure**
```bash
python -m src.cli export tests/rubric.json | head -20
```

### show

Display rubric criteria in human-readable format.

#### Basic Usage

```bash
python -m src.cli show rubric.json
```

#### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `rubric` | Yes | Path to rubric JSON file |

#### Examples

**Display Rubric**
```bash
python -m src.cli show tests/rubric.json
```

**Pipe to Less for Long Rubrics**
```bash
python -m src.cli show tests/rubric.json | less
```

## Global Options

### Help

```bash
# General help
python -m src.cli --help

# Command-specific help
python -m src.cli evaluate --help
python -m src.cli export --help
python -m src.cli show --help
```

## Output Formats

### Pretty Format (Default)

```bash
python -m src.cli evaluate rubric.json -f document.txt
```

Output:
```
Evaluation Results:
----------------------------------------
Model: gpt-3.5-turbo
Document: document.txt
----------------------------------------

claim_clarity: 4/5
  Confidence: 0.85

coherence: 5/5
  Confidence: 0.92

evidence_quality: 3/5
  Confidence: 0.78

----------------------------------------
Overall Score: 4.00/5
```

### JSON Format

```bash
python -m src.cli evaluate rubric.json -f document.txt -o json
```

Output:
```json
{
  "document_id": "document.txt",
  "model_used": "gpt-3.5-turbo",
  "overall_score": 4.0,
  "scores": [
    {
      "criterion_name": "claim_clarity",
      "score": 4,
      "confidence": 0.85,
      "reasoning": "The main argument is clearly stated..."
    }
  ],
  "metadata": {
    "timestamp": "2024-01-15T10:30:00Z",
    "provider": "openai"
  }
}
```

### Verbose Mode

```bash
python -m src.cli evaluate rubric.json -f document.txt -v
```

Includes detailed reasoning for each score:
```
claim_clarity: 4/5
  Confidence: 0.85
  Reasoning: The main argument is clearly stated in the introduction and maintained throughout. Minor ambiguity in the second paragraph slightly reduces clarity.
```

## Provider Configuration

### Pydantic AI (Default)

```bash
# Uses Pydantic AI framework with model auto-detection
python -m src.cli evaluate rubric.json -f document.txt --provider pydantic_ai
```

### OpenAI Direct

```bash
# Direct OpenAI API access
python -m src.cli evaluate rubric.json -f document.txt --provider openai --model gpt-4
```

### Anthropic Direct

```bash
# Direct Anthropic API access
python -m src.cli evaluate rubric.json -f document.txt --provider anthropic --model claude-3-sonnet-20240229
```

## Model Selection

### Default Models

| Provider | Default Model |
|----------|---------------|
| pydantic_ai | gpt-4o-mini |
| openai | gpt-4o-mini |
| anthropic | claude-3-5-haiku-latest |

### Specifying Models

```bash
# OpenAI models
python -m src.cli evaluate rubric.json -f doc.txt --provider openai --model gpt-3.5-turbo
python -m src.cli evaluate rubric.json -f doc.txt --provider openai --model gpt-4
python -m src.cli evaluate rubric.json -f doc.txt --provider openai --model gpt-4-turbo-preview

# Anthropic models
python -m src.cli evaluate rubric.json -f doc.txt --provider anthropic --model claude-3-haiku-20240307
python -m src.cli evaluate rubric.json -f doc.txt --provider anthropic --model claude-3-sonnet-20240229
python -m src.cli evaluate rubric.json -f doc.txt --provider anthropic --model claude-3-opus-20240229
```

## Advanced Usage

### Environment Variables

Set default values using environment variables:

```bash
# .env file
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
DEFAULT_MODEL=gpt-4
DEFAULT_PROVIDER=openai
```

### Batch Processing

```bash
# Evaluate multiple documents
for file in documents/*.txt; do
    echo "Evaluating $file..."
    python -m src.cli evaluate rubric.json -f "$file" -o json > "results/$(basename "$file" .txt).json"
done
```

### Piping and Redirection

```bash
# Save results to file
python -m src.cli evaluate rubric.json -f document.txt > results.txt

# Combine with other tools
python -m src.cli evaluate rubric.json -f document.txt -o json | jq '.overall_score'

# Process multiple files
find documents/ -name "*.txt" -exec python -m src.cli evaluate rubric.json -f {} \; | grep "Overall Score"
```

### Parameter Tuning

```bash
# Lower temperature for more consistent results
python -m src.cli evaluate rubric.json -f document.txt --temperature 0.1

# Higher temperature for more creative evaluation
python -m src.cli evaluate rubric.json -f document.txt --temperature 0.7

# Limit response length
python -m src.cli evaluate rubric.json -f document.txt --max-tokens 1000
```

## Error Handling

### Common Errors and Solutions

#### File Not Found
```bash
$ python -m src.cli evaluate missing_rubric.json -f document.txt
Error: File not found - missing_rubric.json
```
**Solution**: Check file path and ensure file exists.

#### Invalid JSON
```bash
$ python -m src.cli evaluate invalid_rubric.json -f document.txt
Error: JSON decode error in rubric file
```
**Solution**: Validate JSON format using `python -c "import json; json.load(open('rubric.json'))"`

#### Missing API Key
```bash
$ python -m src.cli evaluate rubric.json -f document.txt --provider openai
Error: Failed to initialize LLM provider: OpenAI API key not found
Hint: Make sure API keys are set in environment variables:
  - OpenAI: OPENAI_API_KEY
  - Anthropic: ANTHROPIC_API_KEY
```
**Solution**: Set appropriate environment variables.

#### Empty Document
```bash
$ echo "" | python -m src.cli evaluate rubric.json
Error: Empty document provided
```
**Solution**: Ensure document contains text content.

### Debug Mode

```bash
# Enable verbose output for debugging
python -m src.cli evaluate rubric.json -f document.txt -v

# Check rubric structure
python -m src.cli show rubric.json

# Test with mock mode
python -m src.cli evaluate rubric.json -f document.txt --mock
```

## Integration Examples

### Shell Scripts

```bash
#!/bin/bash
# evaluate_batch.sh

RUBRIC="$1"
INPUT_DIR="$2"
OUTPUT_DIR="$3"

if [ $# -ne 3 ]; then
    echo "Usage: $0 <rubric> <input_dir> <output_dir>"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

for file in "$INPUT_DIR"/*.txt; do
    basename=$(basename "$file" .txt)
    echo "Processing $basename..."
    
    python -m src.cli evaluate "$RUBRIC" -f "$file" -o json > "$OUTPUT_DIR/$basename.json"
    
    if [ $? -eq 0 ]; then
        echo "✓ $basename completed"
    else
        echo "✗ $basename failed"
    fi
done

echo "Batch evaluation complete!"
```

### Python Integration

```python
import subprocess
import json

def cli_evaluate(document_path, rubric_path, provider="pydantic_ai"):
    """Use CLI from Python code"""
    cmd = [
        "python", "-m", "src.cli", "evaluate",
        rubric_path,
        "-f", document_path,
        "--provider", provider,
        "-o", "json"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        raise Exception(f"CLI evaluation failed: {result.stderr}")

# Usage
try:
    results = cli_evaluate("document.txt", "rubric.json", "openai")
    print(f"Score: {results['overall_score']}")
except Exception as e:
    print(f"Error: {e}")
```

### Makefile Integration

```makefile
# Makefile

RUBRIC = tests/rubric.json
DOCS_DIR = documents
RESULTS_DIR = results

.PHONY: evaluate clean show-rubric

evaluate: $(RESULTS_DIR)
	@for doc in $(DOCS_DIR)/*.txt; do \
		name=$$(basename $$doc .txt); \
		echo "Evaluating $$name..."; \
		python -m src.cli evaluate $(RUBRIC) -f $$doc -o json > $(RESULTS_DIR)/$$name.json; \
	done

$(RESULTS_DIR):
	mkdir -p $(RESULTS_DIR)

clean:
	rm -rf $(RESULTS_DIR)

show-rubric:
	python -m src.cli show $(RUBRIC)

# Evaluate single document
eval-%:
	python -m src.cli evaluate $(RUBRIC) -f $(DOCS_DIR)/$*.txt -v
```

### CI/CD Integration

```yaml
# .github/workflows/evaluate.yml
name: Document Evaluation

on:
  pull_request:
    paths:
      - 'documents/**'

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Evaluate documents
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          for file in documents/*.txt; do
            echo "Evaluating $file..."
            python -m src.cli evaluate tests/rubric.json -f "$file" -v
          done
```

## Performance Optimization

### Parallel Processing

```bash
# GNU Parallel
find documents/ -name "*.txt" | parallel -j 4 python -m src.cli evaluate rubric.json -f {} -o json \> results/{/.}.json

# xargs
find documents/ -name "*.txt" | xargs -P 4 -I {} python -m src.cli evaluate rubric.json -f {} -v
```

### Caching Results

```bash
# Create cache directory structure
mkdir -p cache/{openai,anthropic}

# Cached evaluation script
#!/bin/bash
HASH=$(echo "$2" | sha256sum | cut -d' ' -f1)
CACHE_FILE="cache/$1/$HASH.json"

if [ -f "$CACHE_FILE" ]; then
    echo "Cache hit: $CACHE_FILE"
    cat "$CACHE_FILE"
else
    echo "Cache miss, evaluating..."
    python -m src.cli evaluate rubric.json -f "$2" --provider "$1" -o json | tee "$CACHE_FILE"
fi
```

## Quick Reference

### Essential Commands

```bash
# Basic evaluation
python -m src.cli evaluate rubric.json -f document.txt

# JSON output
python -m src.cli evaluate rubric.json -f document.txt -o json

# Verbose mode
python -m src.cli evaluate rubric.json -f document.txt -v

# Specific provider
python -m src.cli evaluate rubric.json -f document.txt --provider openai --model gpt-4

# From stdin
cat document.txt | python -m src.cli evaluate rubric.json

# Show rubric
python -m src.cli show rubric.json

# Export to XML
python -m src.cli export rubric.json -o criteria.xml

# Mock evaluation
python -m src.cli evaluate rubric.json -f document.txt --mock
```

### Common Workflows

```bash
# 1. Check rubric structure
python -m src.cli show rubric.json

# 2. Test with mock mode
python -m src.cli evaluate rubric.json -f sample.txt --mock

# 3. Evaluate with real provider
python -m src.cli evaluate rubric.json -f sample.txt --provider openai

# 4. Get detailed results
python -m src.cli evaluate rubric.json -f sample.txt -v -o json

# 5. Batch process
for f in docs/*.txt; do python -m src.cli evaluate rubric.json -f "$f" -o json > "results/$(basename "$f" .txt).json"; done
```