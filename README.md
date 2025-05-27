# LLM as a Judge

A Python framework for evaluating documents using Large Language Models (LLMs) as judges based on structured criteria.

## Overview

This project provides a flexible evaluation system where LLMs assess documents against predefined criteria. It's designed for scenarios where you need consistent, scalable evaluation of text documents such as essays, reports, or any written content.

## Features

- **Structured Evaluation Framework**: Define evaluation criteria with multiple scoring levels
- **Flexible Scoring System**: 5-point scale evaluation with detailed rules for each level
- **XML Export**: Export evaluation criteria to XML format for interoperability
- **Mock Evaluation Support**: Test your evaluation pipeline without LLM API calls
- **Extensible Architecture**: Easy integration with various LLM providers (OpenAI, Anthropic, etc.)

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
│   └── evaluator.py     # Core evaluation engine
├── tests/
│   ├── rubric.json      # Sample evaluation rubric
│   ├── test_criteria.py # Tests for criteria models
│   └── test_evaluator.py # Tests for evaluation engine
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

## Future Enhancements

- [x] CLI interface
- [ ] Real LLM API integration (OpenAI, Anthropic)
- [ ] Batch evaluation for multiple documents
- [ ] Evaluation result export (JSON/CSV)
- [ ] Evaluation calibration features
- [ ] Multi-evaluator consensus mechanisms

## Acknowledgments

Built with support from Claude (Anthropic) for development and testing.