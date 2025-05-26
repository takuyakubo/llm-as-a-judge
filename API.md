# API Documentation

This document provides detailed API documentation for the LLM as a Judge framework.

## Table of Contents

- [Criteria Module](#criteria-module)
- [Evaluator Module](#evaluator-module)
- [Usage Examples](#usage-examples)
- [Integration Examples](#integration-examples)

## Criteria Module

### Classes

#### `Level`

Represents a scoring level within a criterion.

```python
from src.criteria import Level

level = Level(score=5, rule="Exceptional performance meeting all requirements")
```

**Attributes:**
- `score` (int): Numeric score value (typically 1-5)
- `rule` (str): Description of what qualifies for this score level

#### `Criterion`

Represents a single evaluation criterion.

```python
from src.criteria import Criterion, Level

criterion = Criterion(
    name="clarity",
    description="How clearly the argument is presented",
    levels=[
        Level(score=5, rule="Crystal clear with no ambiguity"),
        Level(score=4, rule="Generally clear with minor issues"),
        Level(score=3, rule="Somewhat clear but needs improvement"),
        Level(score=2, rule="Unclear in many places"),
        Level(score=1, rule="Very unclear throughout")
    ]
)
```

**Attributes:**
- `name` (str): Unique identifier for the criterion
- `description` (str): Detailed description of what this criterion evaluates
- `levels` (List[Level]): List of scoring levels, typically ordered from highest to lowest

**Methods:**
- `to_dict() -> dict`: Convert to dictionary representation
- `to_xml() -> str`: Convert to XML string representation

#### `Criteria`

Container class for managing multiple evaluation criteria.

```python
from src.criteria import Criteria

# Load from JSON file
criteria = Criteria.from_json_file('rubric.json')

# Or create manually
criteria = Criteria(criteria_list=[criterion1, criterion2, ...])
```

**Class Methods:**
- `from_json_file(filepath: str) -> Criteria`: Load criteria from a JSON file
- `from_dict(data: dict) -> Criteria`: Create from dictionary

**Methods:**
- `to_dict() -> dict`: Convert to dictionary
- `to_json(filepath: str)`: Save to JSON file
- `to_xml() -> str`: Export all criteria as XML

## Evaluator Module

### Classes

#### `Evaluator`

Main class for evaluating documents against criteria.

```python
from src.evaluator import Evaluator
from src.criteria import Criteria

criteria = Criteria.from_json_file('rubric.json')
evaluator = Evaluator(criteria, llm_function=my_llm_function)
```

**Constructor Parameters:**
- `criteria` (Criteria): The evaluation criteria to use
- `llm_function` (Optional[Callable[[str], str]]): Function that takes a prompt and returns LLM response. If None, uses mock evaluation.

**Methods:**

##### `generate_prompt(document: str) -> str`

Generates the evaluation prompt for the LLM.

```python
prompt = evaluator.generate_prompt("Your document text here...")
```

##### `parse_llm_response(response: str) -> Dict[str, int]`

Parses the LLM response to extract scores.

```python
scores = evaluator.parse_llm_response(llm_response_text)
# Returns: {'claim_clarity': 4, 'coherence': 3, ...}
```

##### `evaluate_document(document: str) -> Dict[str, int]`

Evaluates a document and returns scores for each criterion.

```python
results = evaluator.evaluate_document("Your document text...")
# Returns: {'claim_clarity': 4, 'coherence': 3, ...}
```

## Usage Examples

### Basic Evaluation

```python
from src.criteria import Criteria
from src.evaluator import Evaluator

# Load criteria
criteria = Criteria.from_json_file('tests/rubric.json')

# Create evaluator with mock evaluation
evaluator = Evaluator(criteria)

# Evaluate a document
document = """
This is my thesis statement. Here are my supporting arguments.
First, I present evidence A. Second, I show evidence B.
In conclusion, my thesis is supported by the evidence.
"""

results = evaluator.evaluate_document(document)
print(results)
# Output: {'claim_clarity': 3, 'coherence': 4, ...}
```

### Custom Criteria

```python
from src.criteria import Criteria, Criterion, Level

# Define custom criterion
custom_criterion = Criterion(
    name="technical_accuracy",
    description="Accuracy of technical information",
    levels=[
        Level(score=5, rule="All technical details are accurate"),
        Level(score=4, rule="Mostly accurate with minor errors"),
        Level(score=3, rule="Generally accurate but some mistakes"),
        Level(score=2, rule="Many technical errors"),
        Level(score=1, rule="Significant technical inaccuracies")
    ]
)

# Create criteria with custom criterion
criteria = Criteria(criteria_list=[custom_criterion])
```

### Export Criteria to XML

```python
# Export criteria definition to XML
xml_output = criteria.to_xml()
print(xml_output)

# Save to file
with open('criteria.xml', 'w', encoding='utf-8') as f:
    f.write(xml_output)
```

## Integration Examples

### OpenAI Integration

```python
import openai
from src.evaluator import Evaluator

def openai_llm_function(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert document evaluator."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

evaluator = Evaluator(criteria, llm_function=openai_llm_function)
```

### Anthropic Claude Integration

```python
import anthropic
from src.evaluator import Evaluator

def claude_llm_function(prompt: str) -> str:
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

evaluator = Evaluator(criteria, llm_function=claude_llm_function)
```

### Batch Processing

```python
def evaluate_multiple_documents(documents: List[str], evaluator: Evaluator) -> List[Dict[str, int]]:
    results = []
    for doc in documents:
        result = evaluator.evaluate_document(doc)
        results.append(result)
    return results

# Usage
documents = ["Document 1 text...", "Document 2 text...", "Document 3 text..."]
all_results = evaluate_multiple_documents(documents, evaluator)
```

### Async Evaluation

```python
import asyncio
from typing import List, Dict

async def async_evaluate(document: str, evaluator: Evaluator) -> Dict[str, int]:
    # Simulate async LLM call
    await asyncio.sleep(0.1)
    return evaluator.evaluate_document(document)

async def batch_evaluate_async(documents: List[str], evaluator: Evaluator) -> List[Dict[str, int]]:
    tasks = [async_evaluate(doc, evaluator) for doc in documents]
    return await asyncio.gather(*tasks)

# Usage
documents = ["Doc 1", "Doc 2", "Doc 3"]
results = asyncio.run(batch_evaluate_async(documents, evaluator))
```

## Error Handling

```python
try:
    results = evaluator.evaluate_document(document)
except ValueError as e:
    print(f"Evaluation failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

1. **Validate Input**: Always validate document content before evaluation
2. **Handle LLM Failures**: Implement retry logic for LLM API calls
3. **Cache Results**: Consider caching evaluation results for identical documents
4. **Monitor Costs**: Track API usage when using commercial LLMs
5. **Prompt Engineering**: Fine-tune prompts for your specific use case

## Extending the Framework

### Custom Response Parser

```python
class CustomEvaluator(Evaluator):
    def parse_llm_response(self, response: str) -> Dict[str, int]:
        # Custom parsing logic
        # For example, handle different response formats
        return custom_parse_function(response)
```

### Adding Metadata

```python
class ExtendedEvaluator(Evaluator):
    def evaluate_document(self, document: str) -> Dict[str, any]:
        scores = super().evaluate_document(document)
        return {
            'scores': scores,
            'timestamp': datetime.now().isoformat(),
            'document_length': len(document),
            'model_used': 'gpt-4'
        }
```