# Your First Evaluation

This tutorial walks you through running your very first document evaluation using LLM as a Judge. By the end, you'll understand the complete evaluation workflow.

## What You'll Learn

- How to prepare documents for evaluation
- Understanding evaluation criteria and rubrics
- Running evaluations with different LLM providers
- Interpreting evaluation results
- Common pitfalls and how to avoid them

## Step-by-Step Tutorial

### Step 1: Environment Check

First, verify your setup is working:

```bash
# Activate your virtual environment
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Verify installation
python -c "from src.criteria import Criteria; print('✓ Installation OK')"

# Check API keys
python -c "import os; print('✓ OpenAI key:', 'Yes' if os.getenv('OPENAI_API_KEY') else 'Missing')"
```

### Step 2: Understand the Sample Rubric

Let's examine the provided rubric to understand how evaluation works:

```bash
cat tests/rubric.json
```

The rubric contains 5 evaluation criteria:

1. **claim_clarity** (主張の明確さ) - How clear is the main argument?
2. **coherence** (一貫性) - How well does the document flow logically?
3. **evidence_quality** (根拠の質) - How reliable is the supporting evidence?
4. **depth_of_reasoning** (推論の深さ) - How thorough is the logical analysis?
5. **readability** (読みやすさ) - How well-formatted and comprehensible is the text?

Each criterion has 5 levels (1-5) with specific rules for scoring.

### Step 3: Prepare Your Document

Create a test document that we can evaluate:

```bash
cat > test_essay.txt << 'EOF'
The Role of Artificial Intelligence in Education

Introduction
Artificial Intelligence (AI) is rapidly transforming various sectors, and education is no exception. This essay argues that AI has the potential to revolutionize education by personalizing learning experiences, automating administrative tasks, and providing intelligent tutoring systems. However, implementation must be carefully managed to address ethical concerns and ensure equitable access.

Personalized Learning
One of AI's most promising applications in education is personalized learning. AI systems can analyze individual student performance data to identify learning patterns, strengths, and weaknesses. For example, platforms like Khan Academy use AI algorithms to adapt content difficulty based on student progress. Research by Bloom (1984) showed that personalized tutoring can improve student performance by two standard deviations compared to traditional classroom instruction.

Automation of Administrative Tasks
AI can significantly reduce the administrative burden on educators. Automated grading systems can handle multiple-choice questions and even essay scoring using natural language processing. This automation frees up valuable time for teachers to focus on instruction and student interaction. According to a study by McKinsey (2020), teachers spend approximately 20-40% of their time on administrative tasks that could be automated.

Intelligent Tutoring Systems
AI-powered tutoring systems provide 24/7 support to students, offering immediate feedback and guidance. These systems can simulate human tutoring behavior while being infinitely patient and available. Carnegie Learning's MATHia platform, for instance, has shown significant improvements in student math performance through adaptive AI tutoring.

Challenges and Considerations
Despite these benefits, AI implementation in education faces several challenges. Privacy concerns regarding student data collection and usage must be addressed. There's also the risk of algorithmic bias that could perpetuate educational inequalities. Additionally, the digital divide means that not all students have equal access to AI-powered educational tools.

Conclusion
AI has tremendous potential to enhance education through personalization, automation, and intelligent support systems. However, successful implementation requires careful attention to ethical considerations, equity issues, and the fundamental goal of education: developing critical thinking and human capabilities that complement AI rather than being replaced by it.

References:
- Bloom, B. S. (1984). The 2 sigma problem: The search for methods of group instruction as effective as one-to-one tutoring.
- McKinsey & Company. (2020). The future of work in America: People and places, today and tomorrow.
EOF
```

### Step 4: Run Your First Evaluation

Now let's evaluate this document using the sample rubric:

```bash
python -m src.cli \
  --document test_essay.txt \
  --rubric tests/rubric.json \
  --provider openai \
  --model gpt-3.5-turbo \
  --output first_evaluation.json \
  --verbose
```

!!! tip "Command Breakdown"
    - `--document`: Path to the document to evaluate
    - `--rubric`: Path to the JSON rubric file
    - `--provider`: LLM provider to use (openai, anthropic)
    - `--model`: Specific model to use (optional)
    - `--output`: Save results to JSON file
    - `--verbose`: Show detailed progress

### Step 5: Examine the Results

Check the evaluation results:

```bash
cat first_evaluation.json
```

You should see output similar to:

```json
{
  "overall_score": 4.4,
  "criteria_scores": {
    "claim_clarity": 5,
    "coherence": 4,
    "evidence_quality": 4,
    "depth_of_reasoning": 5,
    "readability": 4
  },
  "detailed_feedback": {
    "claim_clarity": "The main argument is clearly stated in the introduction and consistently maintained throughout the essay. The thesis about AI's potential to revolutionize education is unambiguous.",
    "coherence": "The essay follows a logical structure with clear sections. Each paragraph builds on the previous one, though transitions could be slightly smoother.",
    "evidence_quality": "Good use of specific examples (Khan Academy, Carnegie Learning) and credible sources (Bloom, McKinsey). Citations are present but could be more comprehensive.",
    "depth_of_reasoning": "Excellent analysis that considers both benefits and challenges. The reasoning is thorough and addresses counterarguments effectively.",
    "readability": "Well-formatted with clear headings and paragraphs. Language is accessible and professional."
  },
  "metadata": {
    "provider": "openai",
    "model": "gpt-3.5-turbo",
    "timestamp": "2024-01-15T10:30:00Z",
    "rubric_file": "tests/rubric.json",
    "document_length": 2847
  }
}
```

### Step 6: Interpret the Results

Let's break down what each score means:

#### Overall Score: 4.4/5
This is excellent! The document demonstrates strong performance across all criteria.

#### Individual Scores:

- **Claim Clarity (5/5)**: Perfect score - the main argument is crystal clear
- **Coherence (4/5)**: Very good structure with minor improvement opportunities
- **Evidence Quality (4/5)**: Good use of examples and sources
- **Depth of Reasoning (5/5)**: Excellent analysis considering multiple perspectives
- **Readability (4/5)**: Well-formatted and accessible

### Step 7: Compare Different Providers

Let's see how different AI providers evaluate the same document:

```bash
# Evaluate with Anthropic Claude
python -m src.cli \
  --document test_essay.txt \
  --rubric tests/rubric.json \
  --provider anthropic \
  --output claude_evaluation.json

# Compare results
echo "OpenAI Results:"
python -c "import json; r=json.load(open('first_evaluation.json')); print(f'Overall: {r[\"overall_score\"]}')"

echo "Claude Results:"  
python -c "import json; r=json.load(open('claude_evaluation.json')); print(f'Overall: {r[\"overall_score\"]}')"
```

### Step 8: Try a Lower Quality Document

Let's see how the system handles a weaker document:

```bash
cat > weak_essay.txt << 'EOF'
AI in Education

AI is good for education. It helps students learn better. Teachers like it too.

AI can grade papers fast. This saves time. Students get feedback quickly.

There are some problems though. Some people worry about privacy. Not everyone has computers.

In conclusion, AI is mostly good for education but has some issues.
EOF
```

```bash
python -m src.cli \
  --document weak_essay.txt \
  --rubric tests/rubric.json \
  --provider openai \
  --output weak_evaluation.json

# Compare scores
echo "Strong essay score:"
python -c "import json; r=json.load(open('first_evaluation.json')); print(f'{r[\"overall_score\"]:.1f}')"

echo "Weak essay score:"
python -c "import json; r=json.load(open('weak_evaluation.json')); print(f'{r[\"overall_score\"]:.1f}')"
```

## Understanding the Evaluation Process

### How the AI Judges Work

1. **Criteria Loading**: The system loads your rubric with scoring rules
2. **Document Analysis**: The AI reads and analyzes your document
3. **Criterion-by-Criterion Evaluation**: Each criterion is scored independently
4. **Feedback Generation**: Detailed explanations are provided for each score
5. **Results Compilation**: Scores are aggregated and formatted

### The XML Prompt Structure

Behind the scenes, your rubric is converted to XML format for the AI:

```xml
<criteria>
  <criterion name="claim_clarity">
    <description>主張の明確さ</description>
    <levels>
      <level score="5">主要な主張が冒頭で明確に提示され、一貫して維持されている</level>
      <level score="4">主要な主張が明確だが、一部で曖昧さがある</level>
      <!-- ... more levels ... -->
    </levels>
  </criterion>
  <!-- ... more criteria ... -->
</criteria>
```

This structured format ensures consistent evaluation across different documents and providers.

## Best Practices

### Document Preparation

1. **Clean Text**: Remove formatting artifacts and ensure readable text
2. **Appropriate Length**: 500-5000 words work best for most rubrics
3. **Complete Thoughts**: Ensure your document represents finished work

### Rubric Selection

1. **Match Purpose**: Choose rubrics appropriate for your document type
2. **Clear Criteria**: Ensure scoring rules are unambiguous
3. **Appropriate Scale**: 5-point scales work well for most evaluations

### Provider Selection

1. **Test Multiple**: Different models may emphasize different aspects
2. **Consider Cost**: Balance evaluation quality with API costs
3. **Consistency**: Use the same provider for comparable evaluations

## Common Issues and Solutions

### Low or Unexpected Scores

```bash
# Check if your document matches the rubric's expectations
# The sample rubric is designed for argumentative essays with evidence

# For other document types, create custom rubrics
# See: docs/usage/rubrics.md
```

### API Errors

```bash
# Check your API key
echo $OPENAI_API_KEY

# Verify internet connection
curl -s https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"
```

### JSON Format Issues

```bash
# Validate your rubric JSON
python -c "
import json
try:
    with open('tests/rubric.json') as f:
        json.load(f)
    print('✓ Valid JSON')
except json.JSONDecodeError as e:
    print(f'✗ JSON Error: {e}')
"
```

## Next Steps

Congratulations! You've completed your first evaluation. Here's what to explore next:

1. **[Create Custom Rubrics](usage/rubrics.md)** - Design criteria for your specific needs
2. **[Batch Processing](advanced/batch.md)** - Evaluate multiple documents efficiently  
3. **[Integration Guide](advanced/integration.md)** - Embed evaluations in your workflow
4. **[CLI Reference](usage/cli.md)** - Master all command-line options

## Quick Reference

### Essential Commands

```bash
# Basic evaluation
python -m src.cli --document FILE --rubric RUBRIC

# With specific provider
python -m src.cli --document FILE --rubric RUBRIC --provider openai

# Save results
python -m src.cli --document FILE --rubric RUBRIC --output results.json

# Multiple documents
python -m src.cli --documents FILE1 FILE2 FILE3 --rubric RUBRIC

# Help
python -m src.cli --help
```

### File Formats

- **Documents**: Plain text (.txt), Markdown (.md), or any text format
- **Rubrics**: JSON format with criteria and levels
- **Output**: JSON format with scores and feedback

Ready to dive deeper? Continue with our [Basic Usage Guide](usage/basic.md)!