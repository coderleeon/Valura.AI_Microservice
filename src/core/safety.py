import re
import time
from typing import Tuple, Optional
from src.models.schemas import SafetyStatus

class SafetyGuard:
    """
    Rule-based safety guard for financial queries.
    Designed to run in <10ms without external calls.
    """
    
    RULES = {
        "insider_trading": [
            r"insider.*(info|tip)", r"non.*public", r"private.*information", r"leak", 
            r"inside.*tip", r"not.*public.*yet"
        ],
        "market_manipulation": [
            r"pump.*dump", r"manipulate.*(price|stock)", r"coordinated.*buy", 
            r"artificial.*volume", r"wash.*trade"
        ],
        "guaranteed_returns": [
            r"guaranteed.*(profit|return)", r"can't.*lose", r"100%.*return", r"no.*risk", 
            r"sure.*thing", r"fixed.*return.*of"
        ],
        "illegal_advice": [
            r"hack", r"bypass.*tax", r"money.*laundering", r"offshore.*secret",
            r"evade.*regulation"
        ]
    }

    def __init__(self):
        # Pre-compile regex for performance
        self.compiled_rules = {
            cat: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
            for cat, patterns in self.RULES.items()
        }

    def check_query(self, query: str) -> SafetyStatus:
        """
        Checks if the query violates any safety rules.
        Includes an educational bypass for definitions and explanations.
        """
        start_time = time.perf_counter()
        
        # Educational bypass: Allow queries that ask for definitions or explanations
        educational_patterns = [r"^what is", r"^explain", r"for school", r"educational"]
        for edu_pattern in educational_patterns:
            if re.search(edu_pattern, query.lower()):
                return SafetyStatus(is_safe=True)

        for category, patterns in self.compiled_rules.items():
            for pattern in patterns:
                if pattern.search(query):
                    duration = (time.perf_counter() - start_time) * 1000
                    # Standard block response format
                    return SafetyStatus(
                        is_safe=False,
                        reason=f"Query flagged for potential {category.replace('_', ' ')}.",
                        category=category
                    )
        
        return SafetyStatus(is_safe=True)

# Singleton instance
safety_guard = SafetyGuard()
