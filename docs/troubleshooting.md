# Troubleshooting

Common issues and solutions when using LLM as a Judge.

## Installation Issues

### Python Version Incompatibility

**Symptoms:**
```bash
ERROR: Package requires a newer version of Python
```

**Solutions:**
```bash
# Check your Python version
python --version

# Ensure Python 3.8 or higher
# Install/upgrade Python if needed
# On macOS with Homebrew:
brew install python3

# On Ubuntu/Debian:
sudo apt update && sudo apt install python3.9

# Create virtual environment with specific version
python3.9 -m venv venv
```

### Dependency Installation Errors

**Symptoms:**
```bash
ERROR: Failed building wheel for package
error: Microsoft Visual C++ 14.0 is required
```

**Solutions:**

=== "Windows"
    ```cmd
    # Install Microsoft C++ Build Tools
    # Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    
    # Alternative: Install via chocolatey
    choco install visualstudio2019buildtools
    
    # Upgrade pip and setuptools
    python -m pip install --upgrade pip setuptools wheel
    ```

=== "macOS"
    ```bash
    # Install Xcode command line tools
    xcode-select --install
    
    # Update pip
    pip install --upgrade pip setuptools wheel
    ```

=== "Linux"
    ```bash
    # Ubuntu/Debian
    sudo apt-get install build-essential python3-dev
    
    # CentOS/RHEL
    sudo yum groupinstall "Development Tools"
    sudo yum install python3-devel
    
    # Update pip
    pip install --upgrade pip setuptools wheel
    ```

### Virtual Environment Issues

**Symptoms:**
```bash
ModuleNotFoundError: No module named 'src'
ImportError: attempted relative import with no known parent package
```

**Solutions:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Verify you're in the project root directory
pwd
# Should show: /path/to/llm-as-a-judge

# Reinstall dependencies
pip install -r requirements.txt

# Run from project root with module syntax
python -m src.cli --help
```

## API Configuration Issues

### Missing API Keys

**Symptoms:**
```bash
Error: Failed to initialize LLM provider: OpenAI API key not found
AuthenticationError: No API key provided
```

**Solutions:**
```bash
# Check if .env file exists
ls -la .env

# Create .env file if missing
cat > .env << 'EOF'
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
EOF

# Verify environment variables
echo $OPENAI_API_KEY
python -c "import os; print('OpenAI key present:', bool(os.getenv('OPENAI_API_KEY')))"

# Alternative: Set environment variables directly
export OPENAI_API_KEY="your_key_here"
export ANTHROPIC_API_KEY="your_key_here"
```

### Invalid API Keys

**Symptoms:**
```bash
AuthenticationError: Incorrect API key provided
Error: Invalid authentication credentials
```

**Solutions:**
```bash
# Verify API key format
# OpenAI keys start with "sk-"
# Anthropic keys start with "sk-ant-"

# Test API connectivity
python -c "
import os
from openai import OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
try:
    models = client.models.list()
    print('✓ OpenAI API key valid')
except Exception as e:
    print(f'✗ OpenAI API error: {e}')
"

# Generate new API keys if needed
# OpenAI: https://platform.openai.com/api-keys
# Anthropic: https://console.anthropic.com/
```

### Network Connectivity Issues

**Symptoms:**
```bash
ConnectionError: Failed to establish a new connection
TimeoutError: Request timed out
```

**Solutions:**
```bash
# Test internet connectivity
curl -I https://api.openai.com/
curl -I https://api.anthropic.com/

# Check firewall/proxy settings
# Corporate networks may block API access

# Use different network if needed
# Increase timeout in your code
python -c "
from src.llm_providers import OpenAIProvider
provider = OpenAIProvider(timeout=60)  # 60 second timeout
"
```

## Evaluation Issues

### Empty or Invalid Documents

**Symptoms:**
```bash
Error: Empty document provided
JSON decode error in rubric file
```

**Solutions:**
```bash
# Check document content
wc -l document.txt
head document.txt

# Ensure file encoding is UTF-8
file document.txt
iconv -f ISO-8859-1 -t UTF-8 document.txt > document_utf8.txt

# Validate rubric JSON
python -c "
import json
try:
    with open('rubric.json') as f:
        data = json.load(f)
    print('✓ Valid JSON')
    print(f'Criteria count: {len(data.get(\"criteria\", []))}')
except json.JSONDecodeError as e:
    print(f'✗ JSON Error: {e}')
"

# Fix common JSON issues
# - Remove trailing commas
# - Escape quotes in strings
# - Check bracket/brace matching
```

### Poor Evaluation Quality

**Symptoms:**
- Inconsistent scores across evaluations
- All documents receive similar scores
- Evaluation feedback is generic

**Solutions:**

#### Improve Rubric Specificity
```json
// Poor rubric level
{
  "score": 4,
  "rule": "Good quality"
}

// Better rubric level
{
  "score": 4,
  "rule": "Arguments are well-supported with 2-3 credible sources, clear reasoning, and mostly logical structure with minor gaps"
}
```

#### Test with Different Providers
```bash
# Compare results across providers
python -m src.cli evaluate rubric.json -f doc.txt --provider openai > openai_result.txt
python -m src.cli evaluate rubric.json -f doc.txt --provider anthropic > anthropic_result.txt

# Check for consistency
diff openai_result.txt anthropic_result.txt
```

#### Adjust Model Parameters
```bash
# Lower temperature for more consistent results
python -m src.cli evaluate rubric.json -f doc.txt --temperature 0.1

# Higher temperature for more nuanced evaluation
python -m src.cli evaluate rubric.json -f doc.txt --temperature 0.7
```

### Rate Limiting Issues

**Symptoms:**
```bash
RateLimitError: Rate limit reached for requests
Error 429: Too Many Requests
```

**Solutions:**
```bash
# Add delays between requests
for file in *.txt; do
    python -m src.cli evaluate rubric.json -f "$file"
    sleep 5  # Wait 5 seconds between evaluations
done

# Use lower-tier models for testing
python -m src.cli evaluate rubric.json -f doc.txt --provider openai --model gpt-3.5-turbo

# Implement exponential backoff in scripts
python -c "
import time
import random

def evaluate_with_retry(document, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Your evaluation code here
            return result
        except RateLimitError:
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            print(f'Rate limited, waiting {wait_time:.1f}s...')
            time.sleep(wait_time)
    raise Exception('Max retries exceeded')
"
```

## Performance Issues

### Slow Evaluation Speed

**Symptoms:**
- Evaluations take much longer than expected
- Timeouts during evaluation

**Solutions:**

#### Choose Faster Models
```bash
# Fast models for quick iteration
python -m src.cli evaluate rubric.json -f doc.txt --provider openai --model gpt-3.5-turbo
python -m src.cli evaluate rubric.json -f doc.txt --provider anthropic --model claude-3-haiku-20240307

# Reduce max tokens for shorter responses
python -m src.cli evaluate rubric.json -f doc.txt --max-tokens 1000
```

#### Optimize Document Length
```bash
# Check document length
wc -w document.txt

# For very long documents, consider summarizing first
python -c "
text = open('long_document.txt').read()
# Take first 5000 words for evaluation
words = text.split()[:5000]
summary = ' '.join(words)
with open('summary.txt', 'w') as f:
    f.write(summary)
"
```

#### Parallel Processing
```bash
# Process multiple documents in parallel
find documents/ -name "*.txt" | xargs -P 4 -I {} python -m src.cli evaluate rubric.json -f {}

# GNU Parallel (if available)
find documents/ -name "*.txt" | parallel -j 4 python -m src.cli evaluate rubric.json -f {}
```

### Memory Issues

**Symptoms:**
```bash
MemoryError: Unable to allocate array
Process killed (OOM)
```

**Solutions:**
```bash
# Monitor memory usage
top -p $(pgrep -f "python.*src.cli")

# Process documents in smaller batches
split -l 10 document_list.txt batch_
for batch in batch_*; do
    while read file; do
        python -m src.cli evaluate rubric.json -f "$file"
    done < "$batch"
done

# Use streaming for large files
python -c "
def process_large_file(filename, chunk_size=5000):
    with open(filename, 'r') as f:
        chunk = []
        for line in f:
            chunk.append(line)
            if len(chunk) >= chunk_size:
                # Process chunk
                chunk_text = ''.join(chunk)
                # Evaluate chunk_text
                chunk = []
        
        # Process remaining chunk
        if chunk:
            chunk_text = ''.join(chunk)
            # Evaluate chunk_text
"
```

## Output and Integration Issues

### JSON Format Errors

**Symptoms:**
```bash
JSONDecodeError: Expecting ',' delimiter
Invalid JSON output from evaluation
```

**Solutions:**
```bash
# Validate JSON output
python -m src.cli evaluate rubric.json -f doc.txt -o json | python -m json.tool

# Save and validate
python -m src.cli evaluate rubric.json -f doc.txt -o json > result.json
python -c "import json; json.load(open('result.json')); print('Valid JSON')"

# Use jq for JSON processing
python -m src.cli evaluate rubric.json -f doc.txt -o json | jq '.overall_score'
```

### Character Encoding Issues

**Symptoms:**
```bash
UnicodeDecodeError: 'utf-8' codec can't decode byte
UnicodeEncodeError: 'ascii' codec can't encode character
```

**Solutions:**
```bash
# Check file encoding
file -I document.txt

# Convert to UTF-8
iconv -f ISO-8859-1 -t UTF-8 document.txt > document_utf8.txt

# Handle encoding in Python
python -c "
import codecs

# Try different encodings
encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
for encoding in encodings:
    try:
        with open('document.txt', 'r', encoding=encoding) as f:
            content = f.read()
        print(f'✓ Successfully read with {encoding}')
        break
    except UnicodeDecodeError:
        print(f'✗ Failed with {encoding}')
"

# Force UTF-8 output
export PYTHONIOENCODING=utf-8
python -m src.cli evaluate rubric.json -f doc.txt
```

## Debugging Tools

### Verbose Mode and Logging

```bash
# Enable verbose output
python -m src.cli evaluate rubric.json -f doc.txt -v

# Mock mode for testing without API calls
python -m src.cli evaluate rubric.json -f doc.txt --mock

# Python logging
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)

# Your evaluation code here with debug output
from src.evaluator import DocumentEvaluator
# ... rest of code
"
```

### Configuration Validation

```bash
# Check environment setup
python -c "
import os
import sys
from dotenv import load_dotenv

print('Python version:', sys.version)
print('Current directory:', os.getcwd())

load_dotenv()
print('OpenAI key present:', bool(os.getenv('OPENAI_API_KEY')))
print('Anthropic key present:', bool(os.getenv('ANTHROPIC_API_KEY')))

try:
    from src.criteria import Criteria
    print('✓ src module importable')
except ImportError as e:
    print(f'✗ Import error: {e}')
"
```

### Health Check Script

```bash
# Create comprehensive health check
cat > health_check.py << 'EOF'
#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path

def health_check():
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 8):
        issues.append(f"Python version {sys.version} < 3.8")
    else:
        print("✓ Python version OK")
    
    # Check current directory
    if not Path("src").exists():
        issues.append("Not in project root (src/ directory not found)")
    else:
        print("✓ Project directory OK")
    
    # Check dependencies
    try:
        import pydantic
        import openai
        import anthropic
        print("✓ Dependencies OK")
    except ImportError as e:
        issues.append(f"Missing dependency: {e}")
    
    # Check environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv('OPENAI_API_KEY') and not os.getenv('ANTHROPIC_API_KEY'):
        issues.append("No API keys found")
    else:
        print("✓ API keys present")
    
    # Check sample files
    if not Path("tests/rubric.json").exists():
        issues.append("Sample rubric not found")
    else:
        try:
            with open("tests/rubric.json") as f:
                json.load(f)
            print("✓ Sample rubric OK")
        except json.JSONDecodeError:
            issues.append("Sample rubric is invalid JSON")
    
    # Try module import
    try:
        from src.criteria import Criteria
        from src.evaluator import DocumentEvaluator
        print("✓ Module imports OK")
    except ImportError as e:
        issues.append(f"Import error: {e}")
    
    if issues:
        print("\n❌ Issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("\n✅ All checks passed!")
        return True

if __name__ == "__main__":
    success = health_check()
    sys.exit(0 if success else 1)
EOF

python health_check.py
```

## Getting Help

### Self-Diagnosis Commands

```bash
# Quick system check
python --version
pip list | grep -E "(pydantic|openai|anthropic)"
echo $OPENAI_API_KEY | cut -c1-10

# Test basic functionality
python -c "from src.criteria import Criteria; print('Import OK')"
python -m src.cli show tests/rubric.json | head -5

# Test with mock mode
python -m src.cli evaluate tests/rubric.json --mock << 'EOF'
This is a test document for evaluation.
It contains multiple sentences to test the framework.
The evaluation should work without API calls in mock mode.
EOF
```

### Community Resources

- **GitHub Issues**: [Report bugs and request features](https://github.com/takuyakubo/llm-as-a-judge/issues)
- **Discussions**: [Community discussions](https://github.com/takuyakubo/llm-as-a-judge/discussions)
- **Documentation**: [Official docs](https://takuyakubo.github.io/llm-as-a-judge)

### Creating Bug Reports

When reporting issues, include:

1. **Environment Information**:
   ```bash
   python --version
   pip freeze | grep -E "(pydantic|openai|anthropic)"
   uname -a  # Linux/macOS
   ```

2. **Error Details**:
   - Full error message and stack trace
   - Command that caused the error
   - Sample input files (if not sensitive)

3. **Expected vs Actual Behavior**:
   - What you expected to happen
   - What actually happened
   - Steps to reproduce

4. **Configuration**:
   - Provider and model used
   - Rubric structure (anonymized if needed)
   - Any custom settings

### Common Support Questions

**Q: Why are my evaluations inconsistent?**
A: Check rubric specificity, try lower temperature settings, and ensure criteria levels are clearly distinguished.

**Q: How can I speed up evaluations?**
A: Use faster models (gpt-3.5-turbo, claude-3-haiku), reduce document length, or implement parallel processing.

**Q: My API costs are too high. What can I do?**
A: Switch to cheaper models, optimize prompts, implement caching, or use shorter evaluation criteria.

**Q: Can I use the framework offline?**
A: Currently requires API access to LLM providers. Mock mode is available for testing without API calls.

**Q: How do I create domain-specific rubrics?**
A: See the [Creating Rubrics](usage/rubrics.md) and [Custom Criteria](advanced/custom-criteria.md) guides for detailed instructions.

## Quick Reference

### Essential Debugging Commands

```bash
# Basic health check
python health_check.py

# Test imports
python -c "from src.criteria import Criteria; print('OK')"

# Validate rubric
python -c "import json; json.load(open('rubric.json')); print('Valid')"

# Test API connectivity
python -c "from src.llm_providers import OpenAIProvider; OpenAIProvider()"

# Mock evaluation
python -m src.cli evaluate rubric.json --mock -f document.txt

# Verbose output
python -m src.cli evaluate rubric.json -f document.txt -v

# Check environment
env | grep -E "(OPENAI|ANTHROPIC)"
```

### Emergency Recovery

```bash
# Reset virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Reset configuration
rm .env
cp .env.example .env
# Edit .env with your API keys

# Test with minimal example
echo "Test document" | python -m src.cli evaluate tests/rubric.json --mock
```