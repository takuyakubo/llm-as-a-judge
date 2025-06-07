# LLM as a Judge

A Python framework for evaluating documents using Large Language Models (LLMs) as judges based on structured criteria.

## Overview

This project provides a flexible evaluation system where LLMs assess documents against predefined criteria. It's designed for scenarios where you need consistent, scalable evaluation of text documents such as essays, reports, or any written content.

## Features

- **Structured Evaluation Framework**: Define evaluation criteria with multiple scoring levels
- **Flexible Scoring System**: 5-point scale evaluation with detailed rules for each level
- **Batch Evaluation**: Process multiple documents efficiently with parallel processing
- **XML/CSV Export**: Export evaluation criteria to XML and results to CSV format
- **Mock Evaluation Support**: Test your evaluation pipeline without LLM API calls
- **Extensible Architecture**: Easy integration with various LLM providers (OpenAI, Anthropic, etc.)
- **Progress Tracking**: Visual progress bars for batch operations
- **Directory Scanning**: Automatically evaluate all documents in a directory

## Installation

```bash
# Clone the repository
git clone https://github.com/takuyakubo/llm-as-a-judge.git
cd llm-as-a-judge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt

# Install the CLI tool (optional)
pip install -e .
```

## Quick Start

```python
from src.criteria import Criteria
from src.evaluator import Evaluator

# Load evaluation criteria from JSON
criteria = Criteria.from_json_file('tests/rubric.json')

# Create an evaluator instance
evaluator = Evaluator(criteria)

# Evaluate a document (using mock evaluation)
document = "Your document text here..."
results = evaluator.evaluate_document(document)

print(results)
# Output: {'claim_clarity': 3, 'coherence': 4, ...}
```

### Batch Evaluation

Evaluate multiple documents at once:

```python
# Evaluate a list of documents
documents = [
    "First document text...",
    "Second document text...",
    "Third document text..."
]
results = evaluator.evaluate_batch(documents, show_progress=True)

# Evaluate documents with IDs
documents = {
    "doc1.txt": "First document text...",
    "doc2.txt": "Second document text..."
}
results = evaluator.evaluate_batch(documents, output_csv="results.csv")

# Evaluate all documents in a directory
results = evaluator.evaluate_directory(
    "./documents",
    pattern="*.txt",
    recursive=True,
    max_concurrent=10
)
```

## Evaluation Criteria

The system evaluates documents based on five key criteria:

1. **Claim Clarity** (`claim_clarity`): How clearly the main argument is presented
2. **Coherence** (`coherence`): Logical flow and paragraph structure
3. **Evidence Quality** (`evidence_quality`): Reliability and citation quality of supporting evidence
4. **Depth of Reasoning** (`depth_of_reasoning`): Thoroughness of logical analysis
5. **Readability** (`readability`): Text formatting and comprehensibility

Each criterion is scored on a 1-5 scale with specific rules for each level.

## Custom LLM Integration

To use your own LLM for evaluation:

```python
def my_llm_function(prompt: str) -> str:
    # Your LLM API call here
    # Return the LLM's response as a string
    pass

evaluator = Evaluator(criteria, llm_function=my_llm_function)
results = evaluator.evaluate_document(document)
```

## Project Structure

```
llm-as-a-judge/
├── src/
│   ├── criteria.py      # Data models for evaluation criteria
│   ├── evaluator.py     # Core evaluation engine
│   ├── llm_providers.py # LLM provider integrations
│   └── cli.py          # Command-line interface
├── tests/
│   ├── rubric.json      # Sample evaluation rubric
│   ├── test_criteria.py # Tests for criteria models
│   ├── test_evaluator.py # Tests for evaluation engine
│   └── test_batch_evaluator.py # Tests for batch evaluation
├── notebooks/           # Jupyter notebooks for experiments
├── requirements.txt     # Python dependencies
└── CLAUDE.md           # Development guidelines
```

## Command Line Interface

After installing with `pip install -e .`, you can use the `llm-judge` command:

### Evaluate a Document

```bash
# Evaluate a document from file
llm-judge evaluate tests/rubric.json -f document.txt

# Evaluate from stdin
echo "Your document text here" | llm-judge evaluate tests/rubric.json

# Output as JSON
llm-judge evaluate tests/rubric.json -f document.txt -o json

# Output as CSV
llm-judge evaluate tests/rubric.json -f document.txt -o csv
```

### Batch Evaluation

Process multiple documents efficiently:

```bash
# Evaluate all .txt files in a directory
llm-judge batch tests/rubric.json -d ./documents/

# Evaluate specific files
llm-judge batch tests/rubric.json -f doc1.txt doc2.txt doc3.txt

# Recursive directory search with pattern
llm-judge batch tests/rubric.json -d ./docs/ -r --pattern "*.md"

# Save results to CSV with progress bar
llm-judge batch tests/rubric.json -d ./documents/ -o results.csv

# Control parallel processing
llm-judge batch tests/rubric.json -d ./documents/ --max-concurrent 10

# Disable progress bar for automation
llm-judge batch tests/rubric.json -d ./documents/ --no-progress
```

### Export Criteria

```bash
# Export criteria to XML (stdout)
llm-judge export tests/rubric.json

# Export to file
llm-judge export tests/rubric.json -o criteria.xml
```

### Show Criteria

```bash
# Display criteria in human-readable format
llm-judge show tests/rubric.json
```

## Testing

Run the test suite:

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_criteria

# Run with verbose output
python -m unittest discover tests -v
```

## API Documentation

For detailed API documentation and usage examples, see [API.md](API.md).

## Advanced Usage

### LLM Provider Configuration

The framework supports multiple LLM providers through Pydantic AI:

```bash
# Use OpenAI (default: gpt-4o-mini)
export OPENAI_API_KEY=your_api_key
llm-judge evaluate tests/rubric.json -f document.txt --provider openai --model gpt-4o

# Use Anthropic Claude
export ANTHROPIC_API_KEY=your_api_key
llm-judge evaluate tests/rubric.json -f document.txt --provider anthropic --model claude-3-5-haiku-latest

# Adjust temperature and max tokens
llm-judge evaluate tests/rubric.json -f document.txt --temperature 0.7 --max-tokens 500
```

### Performance Optimization

For large-scale evaluations:

```python
# Use async processing with custom concurrency
results = evaluator.evaluate_batch(
    documents,
    max_concurrent=20,  # Increase for faster processing
    show_progress=True
)

# Export results directly to CSV to save memory
evaluator.evaluate_batch(
    documents,
    output_csv="results.csv",
    include_reasoning=False  # Reduce file size
)
```

## Future Enhancements

- [x] CLI interface
- [x] LLM API integration (OpenAI, Anthropic via Pydantic AI)
- [x] Batch evaluation for multiple documents
- [x] Evaluation result export (JSON/CSV)
- [ ] Real-world API integration testing
- [ ] Evaluation calibration features
- [ ] Multi-evaluator consensus mechanisms
- [ ] Web interface for evaluation management

## Acknowledgments

Built with support from Claude (Anthropic) for development and testing.