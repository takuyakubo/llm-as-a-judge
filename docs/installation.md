# Installation

This guide will help you install and set up LLM as a Judge on your system.

## Requirements

- Python 3.8 or higher
- pip package manager
- API keys for your chosen LLM provider (OpenAI, Anthropic, etc.)

## Quick Installation

### 1. Clone the Repository

```bash
git clone https://github.com/takuyakubo/llm-as-a-judge.git
cd llm-as-a-judge
```

### 2. Create Virtual Environment

=== "macOS/Linux"

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

=== "Windows"

    ```cmd
    python -m venv venv
    venv\Scripts\activate
    ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with your API keys:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic Configuration  
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Default provider (optional)
DEFAULT_LLM_PROVIDER=openai
```

## API Key Setup

### OpenAI

1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Click "Create new secret key"
3. Copy the key and add it to your `.env` file

### Anthropic Claude

1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Navigate to API Keys section
3. Generate a new API key
4. Add it to your `.env` file

## Verification

Test your installation:

```bash
# Run tests to verify installation
python -m unittest discover tests

# Check CLI functionality
python -m src.cli --help
```

## Platform-Specific Notes

### macOS

If you encounter issues with certain dependencies:

```bash
# Install Xcode command line tools if needed
xcode-select --install

# Update pip to latest version
pip install --upgrade pip
```

### Windows

For Windows users, you may need to install Microsoft C++ Build Tools:

1. Download [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Install with C++ build tools workload

### Linux

Install required system dependencies:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-dev python3-pip

# CentOS/RHEL/Fedora
sudo yum install python3-devel python3-pip
```

## Development Installation

For contributors and developers:

```bash
# Clone with development dependencies
git clone https://github.com/takuyakubo/llm-as-a-judge.git
cd llm-as-a-judge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt  # Additional dev dependencies
```

## Troubleshooting

### Common Issues

**Import Error**: If you see module import errors, ensure:
- Virtual environment is activated
- All dependencies are installed
- You're running commands from the project root

**API Key Issues**: 
- Verify your API keys are correct
- Check that your `.env` file is in the project root
- Ensure no extra spaces in your API keys

**Permission Errors**:
- Use `sudo` for system-wide installations (not recommended)
- Prefer virtual environments for local installations

### Getting Help

If you encounter issues:

1. Check our [Troubleshooting Guide](troubleshooting.md)
2. Search [existing issues](https://github.com/takuyakubo/llm-as-a-judge/issues)
3. Create a [new issue](https://github.com/takuyakubo/llm-as-a-judge/issues/new) with:
   - Your operating system
   - Python version
   - Error messages
   - Steps to reproduce

## Next Steps

Once installed, continue with:

- [Quick Start Guide](quickstart.md) - Run your first evaluation
- [Basic Usage](usage/basic.md) - Learn the fundamentals
- [Creating Rubrics](usage/rubrics.md) - Define evaluation criteria