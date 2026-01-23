"""Simple keyword-based relevance filtering for articles."""

from typing import Dict, Optional

# Keywords for each category
CATEGORY_KEYWORDS = {
    "AI for Medicine": [
        "medical",
        "health",
        "clinical",
        "disease",
        "diagnosis",
        "patient",
        "hospital",
        "therapy",
        "drug",
        "cancer",
        "lesion",
        "imaging",
        "radiology",
        "healthcare",
        "medicine",
        "diagnostic",
        "biomedical",
        "pharmaceutical",
        "epidemiology",
        "medical imaging",
    ],
    "AI for Planet": [
        "climate",
        "environment",
        "sustainability",
        "carbon",
        "energy",
        "renewable",
        "solar",
        "wind",
        "emissions",
        "greenhouse",
        "ecological",
        "conservation",
        "biodiversity",
        "water",
        "ocean",
        "atmospheric",
        "weather",
        "pollution",
        "ecosystem",
        "flood",
        "drought",
        "forest",
        "deforestation",
        "geophysics",
        "earth system",
    ],
    "Green AI": [
        "energy efficient",
        "model compression",
        "pruning",
        "quantization",
        "distillation",
        "carbon footprint",
        "sustainable computing",
        "edge computing",
        "power consumption",
        "green computing",
        "model efficiency",
        "computational cost",
        "training efficiency",
        "inference efficiency",
        "parameter efficient",
        "sparse model",
        "knowledge distillation",
        "neural architecture search",
        "automl",
        "efficient transformer",
        "mobile ai",
        "tinyml",
        "edge ai",
        "carbon emission",
        "energy consumption",
        "gpu power",
        "compute efficient",
    ],
}

# Global keywords that must appear (at least one) for any article to be relevant
# Use word boundaries to avoid false matches (e.g., "arterial" containing "ai")
GLOBAL_KEYWORDS = [
    " ai ",
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "neural network",
    "llm",
    "language model",
    "computer vision",
    "reinforcement learning",
    " ml ",
    "machine-learning",
    "deep-learning",
    "ai-powered",
    "ai-driven",
    "ai-based",
    "ml-based",
]


def calculate_relevance(title: str, content: str) -> Optional[Dict]:
    """
    Calculate relevance of an article based on keywords.

    Args:
        title: Article title
        content: Article abstract/content

    Returns:
        Dictionary with category and confidence, or None if not relevant
        {
            "category": str,
            "confidence": float,
            "relevancy_score": float
        }
    """
    # Combine title and content, lowercase for matching
    # Add spaces at start/end to enable word boundary detection
    text = " " + (title + " " + content).lower() + " "

    # First check: Must contain at least one AI-related keyword
    has_ai_keyword = any(keyword in text for keyword in GLOBAL_KEYWORDS)
    if not has_ai_keyword:
        return None

    # Calculate scores for each category
    category_scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        # Count how many keywords match
        matches = sum(1 for keyword in keywords if keyword in text)
        # Calculate score as percentage of keywords found
        score = (matches / len(keywords)) * 100
        category_scores[category] = score

    # Find best matching category
    best_category = max(category_scores, key=category_scores.get)
    best_score = category_scores[best_category]

    # Threshold: Only accept if at least 5% of category keywords match
    MIN_THRESHOLD = 5.0
    if best_score < MIN_THRESHOLD:
        return None

    # Return classification
    return {
        "category": best_category,
        "confidence": min(best_score / 20, 1.0),  # Normalize to 0-1
        "relevancy_score": min(best_score * 2, 100),  # Scale to 0-100
    }


def is_relevant(title: str, content: str) -> bool:
    """
    Quick check if an article is relevant to any category.

    Args:
        title: Article title
        content: Article content/abstract

    Returns:
        True if relevant, False otherwise
    """
    return calculate_relevance(title, content) is not None


# Test cases
if __name__ == "__main__":
    # Test case 1: Should be AI for Planet
    test1_title = (
        "Naiad: Novel Agentic Intelligent Autonomous System for Inland Water Monitoring"
    )
    test1_content = "We present a novel AI system for monitoring water quality and detecting pollution in rivers and lakes using machine learning."

    result1 = calculate_relevance(test1_title, test1_content)
    print(f"Test 1: {test1_title[:50]}...")
    print(f"Result: {result1}\n")

    # Test case 2: Should be filtered out
    test2_title = "PRISMA: Reinforcement Learning Guided Two-Stage Policy Optimization"
    test2_content = "We propose a multi-agent architecture for open-domain question answering using reinforcement learning."

    result2 = calculate_relevance(test2_title, test2_content)
    print(f"Test 2: {test2_title[:50]}...")
    print(f"Result: {result2}\n")

    # Test case 3: Should be AI for Medicine
    test3_title = "Deep Learning for Skin Lesion Detection"
    test3_content = "A convolutional neural network for automated detection of melanoma in dermatology images using medical imaging data."

    result3 = calculate_relevance(test3_title, test3_content)
    print(f"Test 3: {test3_title[:50]}...")
    print(f"Result: {result3}\n")
