# Contributing

Thank you for your interest in contributing to LLM as a Judge! This guide will help you get started with contributing to the project.

## Ways to Contribute

- **Bug Reports**: Help us identify and fix issues
- **Feature Requests**: Suggest new functionality and improvements
- **Documentation**: Improve existing docs or add new content
- **Code Contributions**: Implement features, fix bugs, add tests
- **Rubric Templates**: Share evaluation criteria for different domains
- **Examples**: Provide usage examples and tutorials

## Getting Started

### Development Setup

1. **Fork and Clone**
   ```bash
   # Fork the repository on GitHub
   git clone https://github.com/YOUR_USERNAME/llm-as-a-judge.git
   cd llm-as-a-judge
   ```

2. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # venv\Scripts\activate   # Windows
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Install development dependencies
   pip install -r requirements-dev.txt  # If available
   
   # Or install common dev tools
   pip install pytest black flake8 mypy pre-commit
   ```

3. **Set Up Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

4. **Create Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or: git checkout -b bugfix/issue-description
   ```

### Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_criteria

# Run with coverage (if pytest-cov installed)
pytest --cov=src tests/

# Run linting
flake8 src/ tests/
black --check src/ tests/
mypy src/
```

## Development Guidelines

### Code Style

We follow Python PEP 8 standards with some additional conventions:

```python
# Use type hints
def evaluate_document(document: str, criteria: Criteria) -> EvaluationResult:
    pass

# Use descriptive variable names
evaluation_result = evaluator.evaluate(document_text)

# Add docstrings for public functions
def create_criterion(name: str, description: str) -> Criterion:
    """
    Create a new evaluation criterion.
    
    Args:
        name: Unique identifier for the criterion
        description: Human-readable description
        
    Returns:
        Configured Criterion object
    """
    pass
```

### Testing Requirements

All contributions should include appropriate tests:

```python
# tests/test_new_feature.py
import unittest
from src.new_module import NewClass

class TestNewFeature(unittest.TestCase):
    
    def setUp(self):
        self.test_instance = NewClass()
    
    def test_basic_functionality(self):
        result = self.test_instance.do_something()
        self.assertEqual(result, expected_value)
    
    def test_error_handling(self):
        with self.assertRaises(ValueError):
            self.test_instance.invalid_operation()
```

### Documentation Standards

- **Docstrings**: All public functions and classes must have docstrings
- **Type Hints**: Use type hints for function parameters and return values
- **Comments**: Explain complex logic with inline comments
- **README Updates**: Update README.md if adding new major features

## Contribution Types

### Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Reproduction Steps**: Step-by-step instructions
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: OS, Python version, package versions
6. **Error Messages**: Full error messages and stack traces

**Template:**
```markdown
## Bug Description
Brief description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Environment
- OS: [e.g., macOS 12.0, Ubuntu 20.04, Windows 10]
- Python: [e.g., 3.9.7]
- LLM as a Judge: [e.g., latest main branch]

## Error Output
```bash
Full error message here
```

## Additional Context
Any other relevant information
```

### Feature Requests

For feature requests, please provide:

1. **Use Case**: Why is this feature needed?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: Other approaches considered
4. **Implementation Ideas**: Technical approach (if any)

### Code Contributions

#### Pull Request Process

1. **Create Issue First**: For major features, create an issue to discuss the approach
2. **Follow Coding Standards**: Ensure code follows project conventions
3. **Add Tests**: Include appropriate test coverage
4. **Update Documentation**: Update relevant documentation
5. **Test Thoroughly**: Ensure all tests pass
6. **Create Pull Request**: Follow the PR template

#### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Related Issues
Fixes #(issue number)

## Testing
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Code is commented where necessary
- [ ] Documentation updated
- [ ] No new warnings introduced
```

### Documentation Contributions

Documentation improvements are always welcome:

#### Types of Documentation Contributions

- **API Documentation**: Improve docstrings and API references
- **User Guides**: Add tutorials and how-to guides
- **Examples**: Provide practical usage examples
- **Troubleshooting**: Add solutions to common problems

#### Documentation Setup

```bash
# Install MkDocs dependencies
pip install mkdocs mkdocs-material mkdocs-mermaid2-plugin

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

### Rubric Contributions

We welcome high-quality rubric templates for different domains:

#### Rubric Contribution Guidelines

1. **Domain Expertise**: Ensure you have expertise in the evaluation domain
2. **Clear Criteria**: Provide specific, actionable evaluation criteria
3. **Comprehensive Levels**: Include all 5 scoring levels with clear distinctions
4. **Validation**: Test the rubric with sample documents
5. **Documentation**: Include usage guidelines and examples

#### Rubric Template

```json
{
  "metadata": {
    "name": "Domain-Specific Evaluation Rubric",
    "description": "Evaluation criteria for [specific domain]",
    "version": "1.0.0",
    "author": "Your Name",
    "domain": "academic/business/creative/technical",
    "target_documents": "Description of suitable documents",
    "usage_notes": "Special considerations for using this rubric"
  },
  "criteria": [
    {
      "name": "criterion_name",
      "description": "What this criterion measures",
      "levels": [
        {
          "score": 5,
          "rule": "Specific description of excellent performance"
        },
        // ... additional levels
      ]
    }
    // ... additional criteria
  ]
}
```

## Project Structure

Understanding the project structure helps with contributions:

```
llm-as-a-judge/
├── src/                    # Main source code
│   ├── criteria.py         # Evaluation criteria classes
│   ├── evaluator.py        # Core evaluation logic
│   ├── llm_providers.py    # LLM provider implementations
│   └── cli.py             # Command-line interface
├── tests/                  # Test suite
│   ├── test_criteria.py   # Criteria tests
│   ├── test_evaluator.py  # Evaluator tests
│   └── rubric.json        # Sample rubric for testing
├── docs/                   # Documentation source
│   ├── index.md           # Homepage
│   ├── usage/             # User guides
│   ├── advanced/          # Advanced topics
│   └── api/               # API reference
├── examples/               # Usage examples
├── requirements.txt        # Python dependencies
├── mkdocs.yml             # Documentation configuration
└── README.md              # Project overview
```

## Release Process

For maintainers and core contributors:

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. **Update Version Numbers**
   ```bash
   # Update version in setup.py, __init__.py, etc.
   ```

2. **Update Changelog**
   ```markdown
   ## [1.2.0] - 2024-01-15
   
   ### Added
   - New feature X
   - New rubric template for Y
   
   ### Changed
   - Improved performance of Z
   
   ### Fixed
   - Bug in evaluation logic
   ```

3. **Run Full Test Suite**
   ```bash
   python -m unittest discover tests
   flake8 src/ tests/
   mypy src/
   ```

4. **Build Documentation**
   ```bash
   mkdocs build
   ```

5. **Create Release**
   ```bash
   git tag v1.2.0
   git push origin v1.2.0
   ```

## Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive environment:

- **Be Respectful**: Treat all participants with respect and courtesy
- **Be Collaborative**: Work together constructively
- **Be Inclusive**: Welcome newcomers and diverse perspectives
- **Be Professional**: Maintain professional communication

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests, discussions
- **Pull Requests**: Code contributions and reviews
- **Discussions**: General questions and community discussions

## Recognition

Contributors are recognized in several ways:

- **Contributors File**: Listed in CONTRIBUTORS.md
- **Release Notes**: Mentioned in significant releases
- **Documentation**: Author attribution in contributed documentation
- **Rubric Credits**: Author credit in contributed rubrics

## Getting Help

If you need help with contributing:

1. **Check Documentation**: Review existing docs and guides
2. **Search Issues**: Look for similar questions or problems
3. **Ask Questions**: Create a discussion or issue for guidance
4. **Join Community**: Participate in project discussions

## Development Tips

### Setting Up IDE

**VS Code Configuration:**
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.unittestEnabled": true,
    "python.testing.unittestArgs": [
        "-v",
        "-s",
        "./tests",
        "-p",
        "test_*.py"
    ]
}
```

### Common Development Tasks

```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/

# Type checking
mypy src/

# Run tests with coverage
pytest --cov=src tests/

# Build documentation locally
mkdocs serve

# Test CLI commands
python -m src.cli evaluate tests/rubric.json --mock -f sample.txt
```

### Debugging

```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use debugger
import pdb; pdb.set_trace()

# Print debug information
print(f"Debug: variable_name = {variable_name}")
```

## Licensing

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (specified in LICENSE file).

## Questions?

If you have questions about contributing:

- Create a [GitHub Discussion](https://github.com/takuyakubo/llm-as-a-judge/discussions)
- Open an [Issue](https://github.com/takuyakubo/llm-as-a-judge/issues) for specific problems
- Check existing documentation and guides

Thank you for contributing to LLM as a Judge! 🎉