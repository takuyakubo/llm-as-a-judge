# Creating Rubrics

Learn how to create and customize evaluation rubrics to match your specific assessment needs.

## What are Rubrics?

Rubrics are structured evaluation frameworks that define:
- **Criteria**: Specific aspects to evaluate (e.g., clarity, evidence, organization)
- **Levels**: Score levels (typically 1-5) with clear descriptive rules
- **Consistency**: Standardized evaluation across different documents and evaluators

## Rubric Structure

### JSON Format

All rubrics are defined in JSON format with this structure:

```json
{
  "criteria": [
    {
      "name": "criterion_name",
      "description": "What this criterion measures",
      "levels": [
        {
          "score": 5,
          "rule": "Description of excellent performance"
        },
        {
          "score": 4,
          "rule": "Description of good performance"
        },
        {
          "score": 3,
          "rule": "Description of satisfactory performance"
        },
        {
          "score": 2,
          "rule": "Description of needs improvement"
        },
        {
          "score": 1,
          "rule": "Description of poor performance"
        }
      ]
    }
  ]
}
```

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Unique identifier for the criterion | `"claim_clarity"` |
| `description` | Human-readable explanation | `"How clearly is the main argument presented?"` |
| `levels` | Array of scoring levels | See levels structure below |

### Levels Structure

| Field | Description | Example |
|-------|-------------|---------|
| `score` | Numeric score (typically 1-5) | `5` |
| `rule` | Specific criteria for this score level | `"Main argument is crystal clear..."` |

## Sample Rubrics

### Academic Essay Rubric

```json
{
  "criteria": [
    {
      "name": "thesis_clarity",
      "description": "How clearly is the main thesis presented?",
      "levels": [
        {
          "score": 5,
          "rule": "Thesis is clearly stated, specific, and compelling"
        },
        {
          "score": 4,
          "rule": "Thesis is clear and specific with minor ambiguity"
        },
        {
          "score": 3,
          "rule": "Thesis is present but somewhat unclear or general"
        },
        {
          "score": 2,
          "rule": "Thesis is vague or difficult to identify"
        },
        {
          "score": 1,
          "rule": "No clear thesis or thesis is confused"
        }
      ]
    },
    {
      "name": "evidence_support",
      "description": "How well does evidence support the argument?",
      "levels": [
        {
          "score": 5,
          "rule": "Strong, relevant evidence from credible sources with proper citations"
        },
        {
          "score": 4,
          "rule": "Good evidence that mostly supports the argument"
        },
        {
          "score": 3,
          "rule": "Adequate evidence with some relevance issues"
        },
        {
          "score": 2,
          "rule": "Limited evidence or poor source quality"
        },
        {
          "score": 1,
          "rule": "Little to no evidence or irrelevant evidence"
        }
      ]
    }
  ]
}
```

### Business Report Rubric

```json
{
  "criteria": [
    {
      "name": "executive_summary",
      "description": "Quality and completeness of executive summary",
      "levels": [
        {
          "score": 5,
          "rule": "Comprehensive summary covering all key points, actionable insights"
        },
        {
          "score": 4,
          "rule": "Good summary covering most key points"
        },
        {
          "score": 3,
          "rule": "Basic summary present but missing some important elements"
        },
        {
          "score": 2,
          "rule": "Incomplete summary with significant gaps"
        },
        {
          "score": 1,
          "rule": "No executive summary or completely inadequate"
        }
      ]
    },
    {
      "name": "data_analysis",
      "description": "Quality of data presentation and analysis",
      "levels": [
        {
          "score": 5,
          "rule": "Thorough analysis with clear visualizations and insights"
        },
        {
          "score": 4,
          "rule": "Good analysis with minor presentation issues"
        },
        {
          "score": 3,
          "rule": "Basic analysis present but lacks depth"
        },
        {
          "score": 2,
          "rule": "Superficial analysis with significant gaps"
        },
        {
          "score": 1,
          "rule": "Poor or missing data analysis"
        }
      ]
    }
  ]
}
```

## Creating Custom Rubrics

### Step 1: Define Your Purpose

Before creating a rubric, clearly define:
- **Document type**: Essays, reports, creative writing, etc.
- **Assessment goals**: What aspects are most important?
- **Audience**: Who will use this rubric?
- **Context**: Academic, professional, creative, etc.

### Step 2: Identify Criteria

Choose 3-7 criteria that capture the most important aspects:

#### Common Criteria Types

**Content Quality**
- Clarity of main argument/message
- Evidence and support quality
- Depth of analysis
- Accuracy and factual correctness

**Organization & Structure**
- Logical flow and coherence
- Introduction and conclusion quality
- Paragraph structure
- Transitions between ideas

**Writing Quality**
- Grammar and mechanics
- Vocabulary and word choice
- Sentence variety and style
- Readability and engagement

**Specific Domain Criteria**
- Citation quality (academic)
- Visual presentation (reports)
- Creativity and originality (creative writing)
- Technical accuracy (technical documents)

### Step 3: Write Clear Level Descriptions

For each criterion, create 5 levels with specific, actionable descriptions:

#### Best Practices for Level Descriptions

✅ **Do:**
- Use specific, observable behaviors
- Focus on quality indicators
- Make distinctions clear between levels
- Use consistent language across criteria

❌ **Don't:**
- Use vague terms like "good" or "bad"
- Make levels too similar
- Include multiple unrelated aspects
- Use judgmental language

#### Example: Good vs. Poor Level Descriptions

**Good Level Description:**
```json
{
  "score": 4,
  "rule": "Arguments are well-supported with 3-4 credible sources, proper citations, and clear connections between evidence and claims"
}
```

**Poor Level Description:**
```json
{
  "score": 4,
  "rule": "Pretty good use of sources"
}
```

### Step 4: Test and Refine

#### Testing Your Rubric

1. **Apply to sample documents**: Test with 3-5 documents of varying quality
2. **Check for consistency**: Multiple evaluations should yield similar scores
3. **Verify discrimination**: Good documents should score higher than poor ones
4. **Review feedback quality**: Are the explanations helpful?

#### Common Issues and Fixes

**Issue: All documents score similarly**
- **Fix**: Make level distinctions more specific
- **Example**: Add quantitative indicators where possible

**Issue: Inconsistent scoring**
- **Fix**: Clarify ambiguous language in level descriptions
- **Example**: Define what "adequate" or "sufficient" means

**Issue: Unhelpful feedback**
- **Fix**: Ensure each level provides actionable guidance
- **Example**: Include specific improvement suggestions

## Advanced Rubric Techniques

### Weighted Criteria

For rubrics where some criteria are more important:

```json
{
  "criteria": [
    {
      "name": "content_quality",
      "description": "Quality of ideas and arguments",
      "weight": 0.4,
      "levels": [...]
    },
    {
      "name": "writing_mechanics",
      "description": "Grammar, spelling, and style",
      "weight": 0.2,
      "levels": [...]
    }
  ]
}
```

### Multi-Dimensional Scoring

For complex evaluations with sub-criteria:

```json
{
  "name": "research_quality",
  "description": "Quality of research and sources",
  "dimensions": [
    {
      "name": "source_credibility",
      "weight": 0.5
    },
    {
      "name": "source_relevance", 
      "weight": 0.3
    },
    {
      "name": "citation_format",
      "weight": 0.2
    }
  ],
  "levels": [...]
}
```

### Conditional Criteria

For rubrics that depend on document type:

```json
{
  "name": "visual_elements",
  "description": "Quality of charts, graphs, and visual aids",
  "applicable_when": "document_type == 'report'",
  "levels": [...]
}
```

## Domain-Specific Examples

### Creative Writing Rubric

```json
{
  "criteria": [
    {
      "name": "narrative_voice",
      "description": "Distinctiveness and consistency of narrative voice",
      "levels": [
        {
          "score": 5,
          "rule": "Unique, compelling voice maintained consistently throughout"
        },
        {
          "score": 4,
          "rule": "Strong voice with minor inconsistencies"
        },
        {
          "score": 3,
          "rule": "Adequate voice but lacks distinctiveness"
        },
        {
          "score": 2,
          "rule": "Weak or inconsistent voice"
        },
        {
          "score": 1,
          "rule": "No discernible narrative voice"
        }
      ]
    },
    {
      "name": "character_development",
      "description": "Depth and believability of character development",
      "levels": [
        {
          "score": 5,
          "rule": "Rich, complex characters with clear motivations and growth"
        },
        {
          "score": 4,
          "rule": "Well-developed characters with good depth"
        },
        {
          "score": 3,
          "rule": "Basic character development present"
        },
        {
          "score": 2,
          "rule": "Limited character development"
        },
        {
          "score": 1,
          "rule": "Flat or poorly developed characters"
        }
      ]
    }
  ]
}
```

### Technical Documentation Rubric

```json
{
  "criteria": [
    {
      "name": "technical_accuracy",
      "description": "Correctness of technical information and procedures",
      "levels": [
        {
          "score": 5,
          "rule": "All technical information is accurate and procedures are correct"
        },
        {
          "score": 4,
          "rule": "Mostly accurate with minor technical errors"
        },
        {
          "score": 3,
          "rule": "Generally accurate but some notable errors"
        },
        {
          "score": 2,
          "rule": "Several technical errors that could mislead users"
        },
        {
          "score": 1,
          "rule": "Significant technical errors or misinformation"
        }
      ]
    },
    {
      "name": "usability",
      "description": "How easy it is for users to follow and apply the documentation",
      "levels": [
        {
          "score": 5,
          "rule": "Clear step-by-step instructions with examples and troubleshooting"
        },
        {
          "score": 4,
          "rule": "Clear instructions with good examples"
        },
        {
          "score": 3,
          "rule": "Basic instructions that are generally followable"
        },
        {
          "score": 2,
          "rule": "Instructions present but unclear or incomplete"
        },
        {
          "score": 1,
          "rule": "Instructions are confusing or missing key steps"
        }
      ]
    }
  ]
}
```

## Using Rubrics Effectively

### Best Practices

1. **Start Simple**: Begin with 3-5 clear criteria
2. **Test Iteratively**: Refine based on actual usage
3. **Document Rationale**: Keep notes on why you chose specific criteria
4. **Share for Feedback**: Get input from other evaluators
5. **Version Control**: Track changes and improvements over time

### Validation Strategies

#### Inter-rater Reliability
```bash
# Test with multiple evaluators
python -m src.cli --document test_doc.txt --rubric my_rubric.json --provider openai > eval1.json
python -m src.cli --document test_doc.txt --rubric my_rubric.json --provider anthropic > eval2.json

# Compare results
python -c "
import json
r1 = json.load(open('eval1.json'))
r2 = json.load(open('eval2.json'))
print(f'Provider 1: {r1[\"overall_score\"]:.2f}')
print(f'Provider 2: {r2[\"overall_score\"]:.2f}')
print(f'Difference: {abs(r1[\"overall_score\"] - r2[\"overall_score\"]):.2f}')
"
```

#### Criterion Correlation Analysis
```python
# Analyze relationships between criteria
import json
import numpy as np

results = []
for file in ['eval1.json', 'eval2.json', 'eval3.json']:
    with open(file) as f:
        data = json.load(f)
        results.append(list(data['criteria_scores'].values()))

# Calculate correlation matrix
correlation_matrix = np.corrcoef(np.array(results).T)
print("Criterion correlations:")
print(correlation_matrix)
```

## Rubric Management

### File Organization

```
rubrics/
├── academic/
│   ├── essay_rubric.json
│   ├── research_paper_rubric.json
│   └── thesis_rubric.json
├── business/
│   ├── report_rubric.json
│   ├── proposal_rubric.json
│   └── memo_rubric.json
├── creative/
│   ├── fiction_rubric.json
│   ├── poetry_rubric.json
│   └── screenplay_rubric.json
└── technical/
    ├── documentation_rubric.json
    ├── api_reference_rubric.json
    └── tutorial_rubric.json
```

### Version Control

```json
{
  "metadata": {
    "version": "1.2.0",
    "created": "2024-01-01",
    "modified": "2024-01-15",
    "author": "Your Name",
    "description": "Academic essay evaluation rubric",
    "changelog": [
      "v1.2.0: Added evidence quality sub-criteria",
      "v1.1.0: Refined thesis clarity descriptions",
      "v1.0.0: Initial version"
    ]
  },
  "criteria": [...]
}
```

### Programmatic Rubric Creation

```python
from src.criteria import Criteria, Criterion, Level

# Create criteria programmatically
def create_essay_rubric():
    thesis_criterion = Criterion(
        name="thesis_clarity",
        description="How clearly is the main thesis presented?",
        levels=[
            Level(score=5, rule="Thesis is clearly stated, specific, and compelling"),
            Level(score=4, rule="Thesis is clear and specific with minor ambiguity"),
            Level(score=3, rule="Thesis is present but somewhat unclear or general"),
            Level(score=2, rule="Thesis is vague or difficult to identify"),
            Level(score=1, rule="No clear thesis or thesis is confused")
        ]
    )
    
    evidence_criterion = Criterion(
        name="evidence_support",
        description="How well does evidence support the argument?",
        levels=[
            Level(score=5, rule="Strong, relevant evidence from credible sources"),
            Level(score=4, rule="Good evidence that mostly supports the argument"),
            Level(score=3, rule="Adequate evidence with some relevance issues"),
            Level(score=2, rule="Limited evidence or poor source quality"),
            Level(score=1, rule="Little to no evidence or irrelevant evidence")
        ]
    )
    
    return Criteria(criteria=[thesis_criterion, evidence_criterion])

# Save to file
rubric = create_essay_rubric()
rubric.to_json_file("my_essay_rubric.json")
```

## Troubleshooting Common Issues

### Issue: Rubric produces inconsistent scores

**Symptoms:**
- Same document gets very different scores on repeated evaluations
- Similar quality documents get vastly different scores

**Solutions:**
1. **Increase specificity** in level descriptions
2. **Add quantitative indicators** where possible
3. **Test with multiple providers** to identify provider-specific biases
4. **Reduce ambiguous language** in criteria descriptions

### Issue: All documents score in the middle range (3s)

**Symptoms:**
- Rarely see scores of 1, 2, 4, or 5
- Poor discrimination between document quality

**Solutions:**
1. **Sharpen level distinctions** - make differences more pronounced
2. **Anchor extremes** - clearly define what constitutes 1 and 5
3. **Use comparative language** - "better than," "worse than"
4. **Test with deliberately poor/excellent examples**

### Issue: Feedback is generic or unhelpful

**Symptoms:**
- Evaluation explanations are vague
- No actionable improvement suggestions

**Solutions:**
1. **Include improvement guidance** in level descriptions
2. **Use specific examples** in criteria definitions
3. **Add context** about why criteria matter
4. **Request specific feedback** in evaluation prompts

## Next Steps

Once you've mastered rubric creation:

1. **[Multiple Providers](providers.md)** - Compare how different AI models interpret your rubrics
2. **[CLI Reference](cli.md)** - Learn advanced command-line options for rubric usage
3. **[Custom Criteria](../advanced/custom-criteria.md)** - Create sophisticated evaluation frameworks
4. **[Batch Evaluation](../advanced/batch.md)** - Use your rubrics to evaluate multiple documents efficiently

## Quick Reference

### Rubric Checklist

✅ **Structure**
- [ ] Valid JSON format
- [ ] Required fields present (name, description, levels)
- [ ] Consistent scoring scale (1-5 recommended)

✅ **Content Quality**
- [ ] Criteria match document type and purpose
- [ ] Level descriptions are specific and actionable
- [ ] Clear distinctions between score levels
- [ ] No ambiguous or subjective language

✅ **Testing**
- [ ] Tested with sample documents of varying quality
- [ ] Consistent results across multiple evaluations
- [ ] Good discrimination between quality levels
- [ ] Helpful and specific feedback

### Essential Commands

```bash
# Validate rubric JSON
python -c "import json; json.load(open('my_rubric.json')); print('✓ Valid JSON')"

# Test rubric with sample document
python -m src.cli --document sample.txt --rubric my_rubric.json

# Compare providers using same rubric
python -m src.cli --document sample.txt --rubric my_rubric.json --provider openai
python -m src.cli --document sample.txt --rubric my_rubric.json --provider anthropic

# Batch test multiple documents
python -m src.cli --documents *.txt --rubric my_rubric.json --output results.json
```