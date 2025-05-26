# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Testing
```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_criteria

# Run tests from project root (ensure src module is importable)
python -m unittest tests.test_criteria.TestCriteria
```

## Architecture

This is an LLM-as-a-Judge evaluation framework for scoring documents based on structured criteria.

### Core Components

**src/criteria.py**: Defines the evaluation framework data models using Pydantic:
- `Level`: Represents a scoring level with score (int) and rule (str)
- `Criterion`: Represents an evaluation criterion with name, description, and levels
- `Criteria`: Container class for managing multiple criterion objects with XML export functionality

**tests/rubric.json**: Contains a complete rubric definition for document logic evaluation with 5 criteria:
- `claim_clarity`: Evaluates how clearly the main argument is presented
- `coherence`: Assesses logical flow and paragraph structure
- `evidence_quality`: Measures the reliability and citation quality of supporting evidence
- `depth_of_reasoning`: Evaluates the thoroughness of logical analysis
- `readability`: Assesses text formatting and comprehensibility

### Data Flow

The system loads evaluation criteria from JSON format (like `rubric.json`) and converts them into structured Pydantic models for programmatic use. The rubric defines 5-point scales for each criterion with specific rules for each scoring level.

### Key Features

**XML Export**: The `Criteria.to_xml()` method exports criteria to XML format:
```xml
<criteria>
  <criterion name="criterion_name">
    <description>Description text</description>
    <levels>
      <level score="5">Rule text</level>
      <level score="4">Rule text</level>
      ...
    </levels>
  </criterion>
  ...
</criteria>
```

### Development Notes

- Tests expect to be run from the project root directory to properly import the `src` module
- Comprehensive unit tests cover XML export functionality with multiple test scenarios
- The current implementation focuses on data modeling and export; evaluation logic is not yet implemented
- Japanese language is used in test data and rubric definitions
- XML export uses Python's built-in `xml.etree.ElementTree` module for reliable XML generation
- When finishing a task or asking something to the user, i.e. when stopping the task by some reasons, use slack to notify the user
- When using slack mcp, always use `<@U27SREZ3R>` to notify the user