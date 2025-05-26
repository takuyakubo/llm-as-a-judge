# Contributing to LLM as a Judge

Thank you for your interest in contributing to the LLM as a Judge project! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Setting Up Your Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/llm-as-a-judge.git
   cd llm-as-a-judge
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # venv\Scripts\activate   # On Windows
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Keep line length under 100 characters

### Project Structure

- `src/`: Core library code
  - `criteria.py`: Data models for evaluation criteria
  - `evaluator.py`: Evaluation engine implementation
- `tests/`: Test files
  - Test files should be named `test_*.py`
  - Use unittest framework for tests
- `notebooks/`: Jupyter notebooks for experiments and demos

### Making Changes

1. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the code style guidelines

3. Write or update tests for your changes

4. Run tests to ensure everything passes:
   ```bash
   python -m unittest discover tests
   ```

5. Commit your changes with a descriptive message:
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

### Commit Message Format

We follow conventional commits format:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `test:` Test additions or modifications
- `refactor:` Code refactoring
- `style:` Code style changes
- `chore:` Maintenance tasks

### Testing

- Write tests for all new functionality
- Ensure all tests pass before submitting PR
- Aim for high test coverage
- Include both unit tests and integration tests where appropriate

### Pull Request Process

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a Pull Request on GitHub

3. Fill out the PR template with:
   - Description of changes
   - Related issue numbers
   - Test plan
   - Any breaking changes

4. Wait for code review and address feedback

5. Once approved, your PR will be merged

## Areas for Contribution

### High Priority

- **LLM API Integration**: Implement connectors for OpenAI, Anthropic, and other LLM providers
- **Batch Processing**: Add support for evaluating multiple documents efficiently
- **CLI Interface**: Create a command-line interface for the tool

### Medium Priority

- **Export Formats**: Add support for CSV, Excel export of evaluation results
- **Prompt Optimization**: Improve evaluation prompts for better accuracy
- **Calibration Features**: Add functionality to ensure evaluation consistency

### Low Priority

- **Visualization**: Create charts and graphs for evaluation results
- **Web Interface**: Build a simple web UI for the tool
- **Multi-language Support**: Extend evaluation to support multiple languages

## Questions and Support

If you have questions:

1. Check existing issues on GitHub
2. Create a new issue with your question
3. Join our discussions in the Issues section

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Respect differing viewpoints and experiences

Thank you for contributing!