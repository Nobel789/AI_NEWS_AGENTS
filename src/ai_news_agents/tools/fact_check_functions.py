"""
Simple fact-checking functions for CrewAI
"""

from typing import Dict, List, Any
from urllib.parse import urlparse


def fact_check_source(url: str, content: str = "") -> Dict[str, Any]:
    """
    Perform fact-checking on a given URL and optionally its content.
    
    Args:
        url (str): The URL to fact-check
        content (str): Optional content to analyze
        
    Returns:
        Dict containing credibility score, bias indicators, and recommendations
    """
    result = {
        "url": url,
        "credibility_score": 0,
        "domain_reputation": "unknown",
        "bias_indicators": [],
        "red_flags": [],
        "recommendations": [],
        "source_type": "unknown",
        "last_updated": "unknown"
    }
    
    try:
        # Analyze domain reputation
        domain_analysis = _analyze_domain(url)
        result.update(domain_analysis)
        
        # Check for bias indicators in content
        if content:
            bias_analysis = _analyze_content_bias(content)
            result.update(bias_analysis)
        
        # Calculate overall credibility score
        result["credibility_score"] = _calculate_credibility_score(result)
        
        # Generate recommendations
        result["recommendations"] = _generate_recommendations(result)
        
    except Exception as e:
        result["error"] = f"Fact-checking failed: {str(e)}"
        result["credibility_score"] = 0
        result["recommendations"] = ["Manual verification required due to analysis error"]
    
    return result


def validate_sources(sources: List[str], topic: str) -> Dict[str, Any]:
    """
    Cross-validate information across multiple sources.
    
    Args:
        sources (List[str]): List of URLs to cross-reference
        topic (str): The topic to validate
        
    Returns:
        Dict containing validation results and consensus analysis
    """
    result = {
        "topic": topic,
        "sources_analyzed": len(sources),
        "consensus_level": "unknown",
        "conflicting_information": [],
        "validated_facts": [],
        "source_diversity": "unknown",
        "recommendation": "unknown"
    }
    
    try:
        # Analyze source diversity
        domains = [urlparse(url).netloc for url in sources]
        unique_domains = len(set(domains))
        
        if unique_domains >= len(sources) * 0.8:  # 80% unique domains
            result["source_diversity"] = "high"
        elif unique_domains >= len(sources) * 0.5:  # 50% unique domains
            result["source_diversity"] = "medium"
        else:
            result["source_diversity"] = "low"
        
        # Determine consensus level based on source count and diversity
        if len(sources) >= 3 and result["source_diversity"] in ["high", "medium"]:
            result["consensus_level"] = "strong"
            result["recommendation"] = "Information appears well-supported across sources"
        elif len(sources) >= 2:
            result["consensus_level"] = "moderate"
            result["recommendation"] = "Seek additional sources for stronger validation"
        else:
            result["consensus_level"] = "weak"
            result["recommendation"] = "Single source - requires significant additional validation"
        
        # Add validation guidance
        if result["source_diversity"] == "low":
            result["conflicting_information"].append("Sources lack diversity - potential echo chamber effect")
        
    except Exception as e:
        result["error"] = f"Source validation failed: {str(e)}"
        result["recommendation"] = "Manual validation required due to analysis error"
    
    return result


def _analyze_domain(url: str) -> Dict[str, Any]:
    """Analyze the domain reputation and characteristics."""
    domain = urlparse(url).netloc.lower()
    
    # Known reputable news sources
    high_credibility_domains = {
        'reuters.com', 'apnews.com', 'bbc.com', 'npr.org', 'pbs.org',
        'wsj.com', 'nytimes.com', 'washingtonpost.com', 'theguardian.com',
        'cnn.com', 'abcnews.go.com', 'cbsnews.com', 'nbcnews.com',
        'techcrunch.com', 'wired.com', 'arstechnica.com', 'nature.com',
        'science.org', 'mit.edu', 'stanford.edu', 'harvard.edu'
    }
    
    # Known biased or low-credibility domains
    low_credibility_indicators = [
        '.blog', 'fake', 'conspiracy', 'truth', 'patriot', 'freedom',
        'real', 'expose', 'leak', 'insider', 'underground'
    ]
    
    result = {
        "domain": domain,
        "domain_reputation": "unknown",
        "source_type": "unknown"
    }
    
    # Check against known high-credibility sources
    for trusted_domain in high_credibility_domains:
        if trusted_domain in domain:
            result["domain_reputation"] = "high"
            result["source_type"] = "established_media"
            break
    
    # Check for low-credibility indicators
    if result["domain_reputation"] == "unknown":
        for indicator in low_credibility_indicators:
            if indicator in domain:
                result["domain_reputation"] = "low"
                result["source_type"] = "questionable"
                break
    
    # Default to medium for unknown domains
    if result["domain_reputation"] == "unknown":
        result["domain_reputation"] = "medium"
        result["source_type"] = "unverified"
    
    return result


def _analyze_content_bias(content: str) -> Dict[str, Any]:
    """Analyze content for bias indicators and red flags."""
    bias_indicators = []
    red_flags = []
    
    # Emotional language indicators
    emotional_words = [
        'shocking', 'devastating', 'incredible', 'unbelievable', 'scandal',
        'outrage', 'fury', 'explosive', 'bombshell', 'exclusive', 'leaked'
    ]
    
    # Conspiracy theory indicators
    conspiracy_indicators = [
        'they don\'t want you to know', 'mainstream media won\'t tell you',
        'hidden truth', 'cover-up', 'secret agenda', 'wake up', 'sheeple'
    ]
    
    # Check for emotional language
    content_lower = content.lower()
    emotional_count = sum(1 for word in emotional_words if word in content_lower)
    if emotional_count > 3:
        bias_indicators.append("High use of emotional language")
    
    # Check for conspiracy indicators
    conspiracy_count = sum(1 for phrase in conspiracy_indicators if phrase in content_lower)
    if conspiracy_count > 0:
        red_flags.append("Contains conspiracy theory language")
    
    # Check for lack of sources
    if not any(phrase in content_lower for phrase in ['according to', 'source:', 'cited', 'reported by', 'study', 'research']):
        red_flags.append("Lacks attribution to sources")
    
    # Check for balanced reporting
    if not any(phrase in content_lower for phrase in ['however', 'although', 'despite', 'on the other hand', 'critics', 'opponents']):
        bias_indicators.append("May lack balanced perspective")
    
    return {
        "bias_indicators": bias_indicators,
        "red_flags": red_flags
    }


def _calculate_credibility_score(analysis: Dict[str, Any]) -> int:
    """Calculate overall credibility score (0-100)."""
    score = 50  # Start with neutral score
    
    # Domain reputation impact
    if analysis["domain_reputation"] == "high":
        score += 30
    elif analysis["domain_reputation"] == "low":
        score -= 40
    elif analysis["domain_reputation"] == "medium":
        score += 10
    
    # Bias indicators impact
    score -= len(analysis.get("bias_indicators", [])) * 10
    
    # Red flags impact
    score -= len(analysis.get("red_flags", [])) * 15
    
    # Ensure score is within bounds
    return max(0, min(100, score))


def _generate_recommendations(analysis: Dict[str, Any]) -> List[str]:
    """Generate recommendations based on analysis."""
    recommendations = []
    
    if analysis["credibility_score"] >= 70:
        recommendations.append("Source appears credible - proceed with confidence")
    elif analysis["credibility_score"] >= 40:
        recommendations.append("Source has moderate credibility - cross-reference with other sources")
        recommendations.append("Verify key claims independently")
    else:
        recommendations.append("Low credibility source - use with extreme caution")
        recommendations.append("Seek verification from multiple reputable sources")
        recommendations.append("Consider excluding from final report")
    
    if analysis.get("red_flags"):
        recommendations.append("Address identified red flags before using content")
    
    if analysis.get("bias_indicators"):
        recommendations.append("Account for potential bias in source presentation")
    
    return recommendations
