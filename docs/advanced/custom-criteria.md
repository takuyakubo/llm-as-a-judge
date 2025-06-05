# Custom Criteria Development

Learn how to create sophisticated evaluation criteria and extend the framework with custom functionality.

## Overview

While the basic rubric system covers most evaluation needs, you may want to create custom criteria that:
- Implement complex scoring algorithms
- Integrate external data sources
- Provide specialized domain expertise
- Offer dynamic evaluation logic

## Programmatic Criteria Creation

### Basic Criterion Construction

```python
from src.criteria import Criterion, Level, Criteria

# Create a simple criterion
def create_readability_criterion():
    return Criterion(
        name="readability",
        description="How easy is the text to read and understand?",
        levels=[
            Level(score=5, rule="Text is very easy to read with clear, concise language"),
            Level(score=4, rule="Text is mostly easy to read with minor complexity"),
            Level(score=3, rule="Text is moderately readable with some difficult passages"),
            Level(score=2, rule="Text is somewhat difficult to read"),
            Level(score=1, rule="Text is very difficult to read and understand")
        ]
    )

# Create rubric with custom criterion
criterion = create_readability_criterion()
criteria = Criteria(criteria=[criterion])

# Save for use
criteria.to_json_file("readability_rubric.json")
```

### Advanced Criterion with Sub-Components

```python
def create_argument_quality_criterion():
    """Create a complex criterion that evaluates multiple aspects of argumentation"""
    
    # Define specific rules for each level
    levels = []
    
    # Level 5: Excellent
    levels.append(Level(
        score=5,
        rule="""
        Argument demonstrates exceptional quality with:
        - Clear, compelling thesis statement
        - Strong evidence from credible sources (3+ academic/professional sources)
        - Sophisticated reasoning with consideration of counterarguments
        - Logical structure with smooth transitions
        - Addresses potential objections thoughtfully
        """
    ))
    
    # Level 4: Good
    levels.append(Level(
        score=4,
        rule="""
        Argument shows good quality with:
        - Clear thesis statement
        - Good evidence from mostly credible sources (2-3 sources)
        - Sound reasoning with some consideration of counterarguments
        - Generally logical structure
        - Addresses some potential objections
        """
    ))
    
    # Level 3: Satisfactory
    levels.append(Level(
        score=3,
        rule="""
        Argument meets basic requirements with:
        - Identifiable thesis statement
        - Adequate evidence from some credible sources (1-2 sources)
        - Basic reasoning present
        - Understandable structure
        - Limited consideration of counterarguments
        """
    ))
    
    # Level 2: Needs Improvement
    levels.append(Level(
        score=2,
        rule="""
        Argument shows weaknesses:
        - Unclear or weak thesis statement
        - Limited evidence or questionable source quality
        - Weak reasoning with logical gaps
        - Poor structure or organization
        - No consideration of counterarguments
        """
    ))
    
    # Level 1: Poor
    levels.append(Level(
        score=1,
        rule="""
        Argument is inadequate:
        - No clear thesis statement
        - Little to no evidence provided
        - Flawed or absent reasoning
        - Confusing or illogical structure
        - No awareness of counterarguments
        """
    ))
    
    return Criterion(
        name="argument_quality",
        description="Overall quality of argumentation including thesis, evidence, reasoning, and structure",
        levels=levels
    )
```

### Domain-Specific Criteria Factory

```python
class CriteriaFactory:
    """Factory for creating domain-specific criteria sets"""
    
    @staticmethod
    def academic_essay_criteria():
        """Create criteria specifically for academic essays"""
        return Criteria(criteria=[
            CriteriaFactory._thesis_clarity(),
            CriteriaFactory._evidence_quality(),
            CriteriaFactory._critical_analysis(),
            CriteriaFactory._academic_writing_style(),
            CriteriaFactory._citation_quality()
        ])
    
    @staticmethod
    def business_report_criteria():
        """Create criteria for business reports"""
        return Criteria(criteria=[
            CriteriaFactory._executive_summary(),
            CriteriaFactory._data_analysis(),
            CriteriaFactory._actionable_recommendations(),
            CriteriaFactory._professional_presentation(),
            CriteriaFactory._stakeholder_consideration()
        ])
    
    @staticmethod
    def creative_writing_criteria():
        """Create criteria for creative writing"""
        return Criteria(criteria=[
            CriteriaFactory._narrative_voice(),
            CriteriaFactory._character_development(),
            CriteriaFactory._plot_structure(),
            CriteriaFactory._dialogue_quality(),
            CriteriaFactory._literary_devices()
        ])
    
    @staticmethod
    def _thesis_clarity():
        return Criterion(
            name="thesis_clarity",
            description="Clarity and strength of the main thesis statement",
            levels=[
                Level(score=5, rule="Thesis is clear, specific, arguable, and compelling"),
                Level(score=4, rule="Thesis is clear and specific with minor weaknesses"),
                Level(score=3, rule="Thesis is present but could be clearer or more specific"),
                Level(score=2, rule="Thesis is unclear or too broad"),
                Level(score=1, rule="No clear thesis or thesis is confused")
            ]
        )
    
    @staticmethod
    def _evidence_quality():
        return Criterion(
            name="evidence_quality",
            description="Quality and relevance of supporting evidence",
            levels=[
                Level(score=5, rule="Strong, relevant evidence from highly credible sources"),
                Level(score=4, rule="Good evidence from credible sources with minor gaps"),
                Level(score=3, rule="Adequate evidence but some quality or relevance issues"),
                Level(score=2, rule="Limited evidence or questionable source quality"),
                Level(score=1, rule="Little to no evidence or unreliable sources")
            ]
        )
    
    # Add more criterion factory methods...

# Usage
academic_criteria = CriteriaFactory.academic_essay_criteria()
business_criteria = CriteriaFactory.business_report_criteria()
creative_criteria = CriteriaFactory.creative_writing_criteria()
```

## Dynamic Criteria Generation

### Context-Aware Criteria

```python
def generate_adaptive_criteria(document_type, document_length, target_audience):
    """Generate criteria based on document characteristics"""
    
    criteria_list = []
    
    # Base criteria for all documents
    criteria_list.append(Criterion(
        name="clarity",
        description="Overall clarity of communication",
        levels=_generate_clarity_levels(target_audience)
    ))
    
    # Length-specific criteria
    if document_length > 5000:  # Long documents
        criteria_list.append(Criterion(
            name="organization",
            description="Document structure and organization",
            levels=_generate_organization_levels_long()
        ))
    else:  # Short documents
        criteria_list.append(Criterion(
            name="conciseness",
            description="Efficiency and conciseness of expression",
            levels=_generate_conciseness_levels()
        ))
    
    # Type-specific criteria
    if document_type == "academic":
        criteria_list.extend([
            _generate_academic_rigor_criterion(),
            _generate_citation_criterion()
        ])
    elif document_type == "business":
        criteria_list.extend([
            _generate_actionability_criterion(),
            _generate_roi_consideration_criterion()
        ])
    elif document_type == "creative":
        criteria_list.extend([
            _generate_creativity_criterion(),
            _generate_emotional_impact_criterion()
        ])
    
    return Criteria(criteria=criteria_list)

def _generate_clarity_levels(audience):
    """Generate clarity levels based on target audience"""
    if audience == "expert":
        return [
            Level(score=5, rule="Complex concepts explained with appropriate technical precision"),
            Level(score=4, rule="Good technical communication with minor unclear points"),
            Level(score=3, rule="Adequate technical communication"),
            Level(score=2, rule="Some technical concepts unclear or imprecise"),
            Level(score=1, rule="Technical communication is unclear or incorrect")
        ]
    elif audience == "general":
        return [
            Level(score=5, rule="Complex ideas explained clearly for general audience"),
            Level(score=4, rule="Generally clear with good explanations"),
            Level(score=3, rule="Mostly clear but some concepts need better explanation"),
            Level(score=2, rule="Several unclear explanations or jargon"),
            Level(score=1, rule="Unclear communication with too much unexplained jargon")
        ]
    else:  # beginner
        return [
            Level(score=5, rule="Concepts explained simply and clearly for beginners"),
            Level(score=4, rule="Clear explanations with good use of examples"),
            Level(score=3, rule="Generally clear but could use more examples"),
            Level(score=2, rule="Some explanations too complex for beginners"),
            Level(score=1, rule="Explanations are too complex or unclear for beginners")
        ]
```

### Weighted Criteria Systems

```python
class WeightedCriteria(Criteria):
    """Extended criteria class with weighting support"""
    
    def __init__(self, criteria_weights):
        """
        criteria_weights: dict mapping criterion_name to (criterion, weight)
        """
        self.criteria_weights = criteria_weights
        criteria_list = [crit for crit, _ in criteria_weights.values()]
        super().__init__(criteria=criteria_list)
    
    def calculate_weighted_score(self, scores_dict):
        """Calculate weighted overall score"""
        total_weight = sum(weight for _, weight in self.criteria_weights.values())
        weighted_sum = 0
        
        for criterion_name, score in scores_dict.items():
            if criterion_name in self.criteria_weights:
                _, weight = self.criteria_weights[criterion_name]
                weighted_sum += score * weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0
    
    def to_dict(self):
        """Export with weight information"""
        base_dict = super().to_dict()
        base_dict['weights'] = {
            name: weight for name, (_, weight) in self.criteria_weights.items()
        }
        return base_dict

# Usage
weighted_criteria = WeightedCriteria({
    "content_quality": (content_criterion, 0.4),
    "writing_style": (style_criterion, 0.3),
    "organization": (org_criterion, 0.2),
    "mechanics": (mechanics_criterion, 0.1)
})
```

## Custom Evaluation Logic

### Conditional Criteria

```python
class ConditionalCriterion(Criterion):
    """Criterion that applies only under certain conditions"""
    
    def __init__(self, name, description, levels, condition_func):
        super().__init__(name, description, levels)
        self.condition_func = condition_func
    
    def applies_to(self, document, metadata=None):
        """Check if this criterion should be applied to the document"""
        return self.condition_func(document, metadata)

def create_citation_criterion():
    """Create criterion that only applies to academic documents"""
    
    def is_academic(document, metadata):
        # Check for academic indicators
        academic_indicators = [
            "abstract", "methodology", "results", "conclusion",
            "references", "bibliography", "doi:", "et al."
        ]
        text_lower = document.lower()
        return any(indicator in text_lower for indicator in academic_indicators)
    
    return ConditionalCriterion(
        name="citation_quality",
        description="Quality and appropriateness of citations",
        levels=[
            Level(score=5, rule="Excellent citation format and source quality"),
            Level(score=4, rule="Good citations with minor format issues"),
            Level(score=3, rule="Adequate citations present"),
            Level(score=2, rule="Poor citation format or quality"),
            Level(score=1, rule="Missing or inadequate citations")
        ],
        condition_func=is_academic
    )

def create_code_quality_criterion():
    """Create criterion for documents containing code"""
    
    def contains_code(document, metadata):
        code_indicators = ["```", "def ", "class ", "function", "#include", "import "]
        return any(indicator in document for indicator in code_indicators)
    
    return ConditionalCriterion(
        name="code_quality",
        description="Quality of code examples and technical accuracy",
        levels=[
            Level(score=5, rule="Code is well-structured, documented, and follows best practices"),
            Level(score=4, rule="Good code quality with minor issues"),
            Level(score=3, rule="Code is functional but could be improved"),
            Level(score=2, rule="Code has significant issues or poor practices"),
            Level(score=1, rule="Code is poorly written or contains errors")
        ],
        condition_func=contains_code
    )
```

### Multi-Dimensional Criteria

```python
class MultiDimensionalCriterion:
    """Criterion that evaluates multiple dimensions separately"""
    
    def __init__(self, name, description, dimensions):
        self.name = name
        self.description = description
        self.dimensions = dimensions  # dict of dimension_name -> Criterion
    
    def to_criteria_list(self):
        """Convert to list of separate criteria for evaluation"""
        criteria_list = []
        for dim_name, criterion in self.dimensions.items():
            # Create a new criterion with combined name
            combined_criterion = Criterion(
                name=f"{self.name}_{dim_name}",
                description=f"{self.description} - {dim_name.replace('_', ' ').title()}",
                levels=criterion.levels
            )
            criteria_list.append(combined_criterion)
        return criteria_list

def create_communication_effectiveness_criterion():
    """Create multi-dimensional communication criterion"""
    
    # Define sub-dimensions
    dimensions = {
        "clarity": Criterion(
            name="clarity",
            description="Clarity of expression",
            levels=[
                Level(score=5, rule="Ideas expressed with exceptional clarity"),
                Level(score=4, rule="Ideas mostly clear with minor ambiguity"),
                Level(score=3, rule="Ideas generally clear but some confusion"),
                Level(score=2, rule="Ideas somewhat unclear"),
                Level(score=1, rule="Ideas are confusing or unclear")
            ]
        ),
        "persuasiveness": Criterion(
            name="persuasiveness", 
            description="Persuasive power of arguments",
            levels=[
                Level(score=5, rule="Highly persuasive with compelling arguments"),
                Level(score=4, rule="Generally persuasive with good arguments"),
                Level(score=3, rule="Moderately persuasive"),
                Level(score=2, rule="Somewhat persuasive but weak arguments"),
                Level(score=1, rule="Not persuasive or unconvincing")
            ]
        ),
        "engagement": Criterion(
            name="engagement",
            description="Reader engagement and interest",
            levels=[
                Level(score=5, rule="Highly engaging and captures reader interest"),
                Level(score=4, rule="Generally engaging with good reader appeal"),
                Level(score=3, rule="Moderately engaging"),
                Level(score=2, rule="Somewhat engaging but could be improved"),
                Level(score=1, rule="Not engaging or difficult to maintain interest")
            ]
        )
    }
    
    return MultiDimensionalCriterion(
        name="communication_effectiveness",
        description="Overall effectiveness of communication",
        dimensions=dimensions
    )
```

## External Data Integration

### External Source Validation

```python
import requests
from typing import Optional

class FactCheckCriterion(Criterion):
    """Criterion that verifies factual claims against external sources"""
    
    def __init__(self, fact_check_api_key: Optional[str] = None):
        self.api_key = fact_check_api_key
        super().__init__(
            name="factual_accuracy",
            description="Accuracy of factual claims and statements",
            levels=[
                Level(score=5, rule="All factual claims verified and accurate"),
                Level(score=4, rule="Most claims accurate with minor inaccuracies"),
                Level(score=3, rule="Generally accurate but some questionable claims"),
                Level(score=2, rule="Several inaccurate or unverified claims"),
                Level(score=1, rule="Many inaccurate claims or misinformation")
            ]
        )
    
    def extract_factual_claims(self, document):
        """Extract potential factual claims from document"""
        # Simple heuristic - look for specific patterns
        import re
        
        # Patterns that often indicate factual claims
        patterns = [
            r'\d+\s*%',  # Percentages
            r'\d+\s*(million|billion|thousand)',  # Large numbers
            r'studies show',  # Research claims
            r'according to',  # Attribution
            r'in \d{4}',  # Year references
        ]
        
        claims = []
        for pattern in patterns:
            matches = re.finditer(pattern, document, re.IGNORECASE)
            for match in matches:
                # Extract surrounding context
                start = max(0, match.start() - 50)
                end = min(len(document), match.end() + 50)
                context = document[start:end].strip()
                claims.append(context)
        
        return claims
    
    def verify_claims(self, claims):
        """Verify claims against external sources"""
        if not self.api_key:
            return {"verified": 0, "total": len(claims), "accuracy_score": 3}
        
        # Placeholder for actual fact-checking API integration
        # This would integrate with services like:
        # - Google Fact Check Tools API
        # - PolitiFact API
        # - Custom fact-checking services
        
        verified_count = 0
        for claim in claims:
            # Simulate API call
            if self._check_claim_via_api(claim):
                verified_count += 1
        
        accuracy_ratio = verified_count / len(claims) if claims else 1.0
        
        # Convert to 1-5 scale
        if accuracy_ratio >= 0.9:
            score = 5
        elif accuracy_ratio >= 0.8:
            score = 4
        elif accuracy_ratio >= 0.6:
            score = 3
        elif accuracy_ratio >= 0.4:
            score = 2
        else:
            score = 1
        
        return {
            "verified": verified_count,
            "total": len(claims),
            "accuracy_score": score,
            "accuracy_ratio": accuracy_ratio
        }
    
    def _check_claim_via_api(self, claim):
        """Check individual claim via fact-checking API"""
        # Placeholder implementation
        # Real implementation would make API calls to fact-checking services
        return True  # Assume verified for now
```

### Language Quality Integration

```python
import textstat
from typing import Dict, Any

class ReadabilityMetricsCriterion(Criterion):
    """Criterion that uses computational linguistics metrics"""
    
    def __init__(self):
        super().__init__(
            name="readability_metrics",
            description="Computational readability and linguistic quality metrics",
            levels=[
                Level(score=5, rule="Excellent readability scores across all metrics"),
                Level(score=4, rule="Good readability with minor areas for improvement"),
                Level(score=3, rule="Average readability scores"),
                Level(score=2, rule="Below average readability"),
                Level(score=1, rule="Poor readability scores")
            ]
        )
    
    def calculate_metrics(self, document: str) -> Dict[str, Any]:
        """Calculate various readability metrics"""
        metrics = {
            "flesch_kincaid": textstat.flesch_kincaid().grade(document),
            "flesch_reading_ease": textstat.flesch_reading_ease(document),
            "gunning_fog": textstat.gunning_fog(document),
            "automated_readability": textstat.automated_readability_index(document),
            "avg_sentence_length": textstat.avg_sentence_length(document),
            "avg_syllables_per_word": textstat.avg_syllables_per_word(document),
            "difficult_words": textstat.difficult_words(document)
        }
        
        return metrics
    
    def interpret_metrics(self, metrics: Dict[str, Any]) -> int:
        """Convert metrics to 1-5 score"""
        # Flesch Reading Ease interpretation
        ease_score = metrics["flesch_reading_ease"]
        
        if ease_score >= 80:  # Very easy
            ease_rating = 5
        elif ease_score >= 70:  # Easy
            ease_rating = 4
        elif ease_score >= 60:  # Standard
            ease_rating = 3
        elif ease_score >= 30:  # Difficult
            ease_rating = 2
        else:  # Very difficult
            ease_rating = 1
        
        # Grade level interpretation
        grade_level = metrics["flesch_kincaid"]
        if grade_level <= 8:  # Middle school
            grade_rating = 5
        elif grade_level <= 12:  # High school
            grade_rating = 4
        elif grade_level <= 16:  # College
            grade_rating = 3
        elif grade_level <= 20:  # Graduate
            grade_rating = 2
        else:  # Advanced graduate
            grade_rating = 1
        
        # Average the ratings
        combined_score = (ease_rating + grade_rating) / 2
        return round(combined_score)
```

## Evaluation Pipeline Customization

### Custom Evaluation Engine

```python
class CustomEvaluationEngine:
    """Extended evaluation engine with custom logic"""
    
    def __init__(self, criteria, llm_provider, custom_processors=None):
        self.criteria = criteria
        self.llm_provider = llm_provider
        self.custom_processors = custom_processors or []
    
    def evaluate(self, document, metadata=None):
        """Evaluate document with custom processing pipeline"""
        results = {}
        
        # Phase 1: Pre-processing
        processed_document = self._preprocess_document(document)
        
        # Phase 2: Standard LLM evaluation
        standard_results = self._standard_evaluation(processed_document)
        results.update(standard_results)
        
        # Phase 3: Custom processors
        for processor in self.custom_processors:
            processor_results = processor.process(document, metadata)
            results.update(processor_results)
        
        # Phase 4: Post-processing and aggregation
        final_results = self._postprocess_results(results, document)
        
        return final_results
    
    def _preprocess_document(self, document):
        """Apply pre-processing steps"""
        # Clean up text, normalize formatting, etc.
        processed = document.strip()
        
        # Remove excessive whitespace
        import re
        processed = re.sub(r'\s+', ' ', processed)
        
        return processed
    
    def _standard_evaluation(self, document):
        """Perform standard LLM-based evaluation"""
        # Use existing DocumentEvaluator logic
        from src.evaluator import DocumentEvaluator
        evaluator = DocumentEvaluator(self.llm_provider, self.criteria)
        return evaluator.evaluate(document)
    
    def _postprocess_results(self, results, original_document):
        """Apply post-processing and result aggregation"""
        # Combine results from different processors
        # Apply custom scoring logic
        # Generate final recommendations
        
        return results

class CustomProcessor:
    """Base class for custom evaluation processors"""
    
    def process(self, document, metadata=None):
        """Process document and return evaluation results"""
        raise NotImplementedError

class SentimentAnalysisProcessor(CustomProcessor):
    """Processor that analyzes document sentiment"""
    
    def process(self, document, metadata=None):
        # Implement sentiment analysis
        # Could use libraries like VADER, TextBlob, or transformers
        
        # Placeholder implementation
        sentiment_score = 0.5  # Neutral
        
        if sentiment_score > 0.6:
            tone_rating = 5  # Very positive
        elif sentiment_score > 0.2:
            tone_rating = 4  # Positive
        elif sentiment_score > -0.2:
            tone_rating = 3  # Neutral
        elif sentiment_score > -0.6:
            tone_rating = 2  # Negative
        else:
            tone_rating = 1  # Very negative
        
        return {
            "sentiment_score": sentiment_score,
            "tone_rating": tone_rating,
            "emotional_appeal": tone_rating
        }
```

## Testing Custom Criteria

### Unit Testing Framework

```python
import unittest
from src.criteria import Criterion, Level

class TestCustomCriteria(unittest.TestCase):
    
    def setUp(self):
        self.sample_criterion = Criterion(
            name="test_criterion",
            description="Test criterion for validation",
            levels=[
                Level(score=5, rule="Excellent performance"),
                Level(score=4, rule="Good performance"),
                Level(score=3, rule="Average performance"),
                Level(score=2, rule="Below average performance"),
                Level(score=1, rule="Poor performance")
            ]
        )
    
    def test_criterion_creation(self):
        """Test basic criterion creation"""
        self.assertEqual(self.sample_criterion.name, "test_criterion")
        self.assertEqual(len(self.sample_criterion.levels), 5)
        self.assertEqual(self.sample_criterion.levels[0].score, 5)
    
    def test_criterion_validation(self):
        """Test criterion validation logic"""
        # Test that all score levels are present
        scores = [level.score for level in self.sample_criterion.levels]
        self.assertEqual(sorted(scores), [1, 2, 3, 4, 5])
        
        # Test that all rules are non-empty
        for level in self.sample_criterion.levels:
            self.assertTrue(len(level.rule.strip()) > 0)
    
    def test_xml_export(self):
        """Test XML export functionality"""
        xml_output = self.sample_criterion.to_xml()
        self.assertIn("test_criterion", xml_output)
        self.assertIn("Excellent performance", xml_output)
    
    def test_conditional_criterion(self):
        """Test conditional criterion application"""
        def always_true(doc, meta):
            return True
        
        def always_false(doc, meta):
            return False
        
        conditional_true = ConditionalCriterion(
            "test", "Test", [Level(5, "Good")], always_true
        )
        conditional_false = ConditionalCriterion(
            "test", "Test", [Level(5, "Good")], always_false
        )
        
        self.assertTrue(conditional_true.applies_to("test document"))
        self.assertFalse(conditional_false.applies_to("test document"))

class TestCriteriaIntegration(unittest.TestCase):
    
    def test_weighted_criteria(self):
        """Test weighted criteria calculation"""
        criterion1 = Criterion("c1", "Test 1", [Level(5, "Good")])
        criterion2 = Criterion("c2", "Test 2", [Level(5, "Good")])
        
        weighted = WeightedCriteria({
            "c1": (criterion1, 0.7),
            "c2": (criterion2, 0.3)
        })
        
        scores = {"c1": 4, "c2": 2}
        weighted_score = weighted.calculate_weighted_score(scores)
        
        expected = (4 * 0.7 + 2 * 0.3) / 1.0
        self.assertAlmostEqual(weighted_score, expected)
    
    def test_multi_dimensional_criterion(self):
        """Test multi-dimensional criterion expansion"""
        dimensions = {
            "clarity": Criterion("clarity", "Clear", [Level(5, "Clear")]),
            "depth": Criterion("depth", "Deep", [Level(5, "Deep")])
        }
        
        multi_dim = MultiDimensionalCriterion(
            "communication", "Communication quality", dimensions
        )
        
        criteria_list = multi_dim.to_criteria_list()
        self.assertEqual(len(criteria_list), 2)
        self.assertEqual(criteria_list[0].name, "communication_clarity")
        self.assertEqual(criteria_list[1].name, "communication_depth")

if __name__ == '__main__':
    unittest.main()
```

### Validation Tools

```python
def validate_criteria_consistency(criteria_list):
    """Validate that criteria are consistent and well-formed"""
    issues = []
    
    for criterion in criteria_list:
        # Check score continuity
        scores = [level.score for level in criterion.levels]
        if sorted(scores) != list(range(1, max(scores) + 1)):
            issues.append(f"{criterion.name}: Non-continuous score levels")
        
        # Check rule clarity
        for level in criterion.levels:
            if len(level.rule.split()) < 3:
                issues.append(f"{criterion.name} level {level.score}: Rule too short")
        
        # Check for duplicate names
        names = [c.name for c in criteria_list]
        if len(names) != len(set(names)):
            issues.append("Duplicate criterion names detected")
    
    return issues

def test_criteria_discrimination(criteria, test_documents):
    """Test how well criteria discriminate between documents of different quality"""
    from src.evaluator import DocumentEvaluator
    from src.llm_providers import OpenAIProvider
    
    provider = OpenAIProvider()
    evaluator = DocumentEvaluator(provider, criteria)
    
    results = []
    for doc_id, document in test_documents.items():
        result = evaluator.evaluate(document)
        results.append((doc_id, result.overall_score))
    
    # Check for score distribution
    scores = [score for _, score in results]
    score_range = max(scores) - min(scores)
    
    analysis = {
        "score_range": score_range,
        "mean_score": sum(scores) / len(scores),
        "results": results,
        "discrimination_quality": "good" if score_range >= 2.0 else "poor"
    }
    
    return analysis
```

## Best Practices

### Design Principles

1. **Specificity**: Make criteria specific and actionable
2. **Objectivity**: Minimize subjective interpretation
3. **Relevance**: Ensure criteria match evaluation goals
4. **Scalability**: Design for consistent application across documents
5. **Transparency**: Make scoring logic clear and explainable

### Performance Considerations

```python
# Efficient criterion processing
class OptimizedCriterion(Criterion):
    """Criterion optimized for batch processing"""
    
    def __init__(self, name, description, levels, cache_enabled=True):
        super().__init__(name, description, levels)
        self.cache_enabled = cache_enabled
        self._xml_cache = None
    
    def to_xml(self):
        """Cached XML export"""
        if self.cache_enabled and self._xml_cache is not None:
            return self._xml_cache
        
        xml = super().to_xml()
        if self.cache_enabled:
            self._xml_cache = xml
        
        return xml
    
    def precompute_features(self, document):
        """Pre-compute features for efficient evaluation"""
        features = {
            "word_count": len(document.split()),
            "sentence_count": len([s for s in document.split('.') if s.strip()]),
            "paragraph_count": len([p for p in document.split('\n\n') if p.strip()])
        }
        return features
```

### Documentation Standards

```python
def create_documented_criterion(name, description, domain_info=None):
    """
    Create a well-documented criterion with metadata
    
    Args:
        name: Unique identifier for the criterion
        description: Human-readable description
        domain_info: Optional domain-specific information
    
    Returns:
        Criterion with embedded documentation
    """
    
    # Example: Academic writing criterion
    if name == "academic_rigor":
        levels = [
            Level(
                score=5,
                rule="""
                Demonstrates exceptional academic rigor through:
                - Sophisticated theoretical framework
                - Rigorous methodology (where applicable)
                - Critical engagement with scholarly literature
                - Original insights or contributions
                - Precise academic language and terminology
                """
            ),
            # ... other levels
        ]
        
        criterion = Criterion(name, description, levels)
        
        # Add metadata
        criterion.metadata = {
            "domain": "academic",
            "complexity": "high",
            "primary_indicators": [
                "theoretical framework",
                "methodology",
                "literature engagement",
                "originality",
                "academic language"
            ],
            "common_pitfalls": [
                "Lack of theoretical grounding",
                "Weak methodology",
                "Insufficient literature review",
                "Casual language"
            ],
            "examples": {
                "excellent": "PhD dissertation with novel theoretical contribution",
                "poor": "Undergraduate essay with no citations"
            }
        }
        
        return criterion
```

## Next Steps

After mastering custom criteria development:

1. **[Batch Processing](batch.md)** - Apply custom criteria to multiple documents
2. **[Integration Guide](integration.md)** - Embed custom criteria in workflows
3. **[API Reference](../api/core.md)** - Deep dive into framework internals
4. **[Contributing Guide](../contributing.md)** - Contribute custom criteria to the project

## Quick Reference

### Custom Criterion Template

```python
def create_my_criterion():
    return Criterion(
        name="my_criterion",
        description="What this criterion measures",
        levels=[
            Level(score=5, rule="Excellent: specific description"),
            Level(score=4, rule="Good: specific description"),
            Level(score=3, rule="Satisfactory: specific description"),
            Level(score=2, rule="Needs improvement: specific description"),
            Level(score=1, rule="Poor: specific description")
        ]
    )
```

### Factory Pattern Example

```python
class MyCriteriaFactory:
    @staticmethod
    def create_domain_criteria():
        return Criteria(criteria=[
            MyCriteriaFactory._criterion1(),
            MyCriteriaFactory._criterion2()
        ])
    
    @staticmethod
    def _criterion1():
        return Criterion(...)
```

### Testing Template

```python
def test_my_criterion():
    criterion = create_my_criterion()
    
    # Test creation
    assert criterion.name == "my_criterion"
    assert len(criterion.levels) == 5
    
    # Test validation
    issues = validate_criteria_consistency([criterion])
    assert len(issues) == 0
    
    # Test discrimination
    test_docs = {"good": "...", "poor": "..."}
    analysis = test_criteria_discrimination(
        Criteria([criterion]), test_docs
    )
    assert analysis["discrimination_quality"] == "good"
```