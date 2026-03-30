"""
Simple sentiment analyzer for provider reviews.
Uses keyword-based scoring (no external libraries).
"""

class SentimentAnalyzer:
    def __init__(self):
        # Expanded word lists for better coverage in a service-provider context
        self.positive_words = [
            "good", "great", "excellent", "best", "amazing", "professional",
            "clean", "fast", "quick", "reliable", "friendly", "skilled",
            "recommend", "highly", "perfect", "spotless", "punctual", 
            "courteous", "efficient", "honest", "fair"
        ]
        self.negative_words = [
            "bad", "poor", "worst", "slow", "late", "unprofessional",
            "dirty", "expensive", "broke", "again", "average",
            "disappointed", "delay", "problem", "rude", "overpriced",
            "messy", "unresponsive", "careless", "no-show"
        ]

    def analyze_sentiment(self, text: str) -> dict:
        """
        Calculates sentiment score and returns a label.
        Returns:
            {
                "label": "positive" | "neutral" | "negative",
                "score": float between -1.0 and 1.0
            }
        """
        if not text or not isinstance(text, str):
            return {"label": "neutral", "score": 0.0}

        low = text.lower()
        # Count occurrences of keywords
        pos_count = sum(1 for word in self.positive_words if word in low)
        neg_count = sum(1 for word in self.negative_words if word in low)
        total = pos_count + neg_count

        if total == 0:
            return {"label": "neutral", "score": 0.0}

        # Calculate score: (Pos - Neg) / Total
        raw_score = (pos_count - neg_count) / total

        # Determine label based on score thresholds
        if raw_score > 0.1:
            label = "positive"
        elif raw_score < -0.1:
            label = "negative"
        else:
            label = "neutral"

        return {
            "label": label, 
            "score": round(raw_score, 2)
        }

    def get_key_phrases(self, text: str) -> list:
        """
        Identifies which specific keywords from our lists triggered the sentiment.
        Used for the 'Keywords Detected' section in the Streamlit UI.
        """
        if not text or not isinstance(text, str):
            return ["—"]

        low = text.lower()
        
        # Collect all keywords present in the text
        found_keywords = [word for word in self.positive_words if word in low]
        found_keywords += [word for word in self.negative_words if word in low]
        
        # Remove duplicates while preserving order
        unique_keywords = list(dict.fromkeys(found_keywords))

        return unique_keywords if unique_keywords else ["—"]