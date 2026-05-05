import json
from typing import Dict, Any, List
from src.models.schemas import PortfolioData, AgentResponse

class PortfolioHealthAgent:
    """
    Analyzes portfolio health and returns structured JSON output.
    Resilient to empty portfolios and produces beginner-friendly insights.
    """
    
    BENCHMARK_RETURN = 0.08  # Static 8% S&P 500 benchmark

    def run(self, portfolio: PortfolioData) -> AgentResponse:
        # Handle empty portfolio with BUILD guidance
        if not portfolio.items:
            content = {
                "message": "Your portfolio is empty. Let's build your financial future!",
                "guidance": [
                    "Step 1: Research low-cost Index Funds or ETFs.",
                    "Step 2: Start with a small, consistent monthly investment.",
                    "Step 3: Diversify across different sectors like Tech, Health, and Energy."
                ],
                "status": "empty_portfolio"
            }
            return AgentResponse(content=json.dumps(content), metadata={"status": "empty_portfolio"})

        # 1. Position Analysis
        sorted_items = sorted(portfolio.items, key=lambda x: x.quantity * x.price, reverse=True)
        total_value = sum(item.quantity * item.price for item in portfolio.items)
        
        top_pos_pct = (sorted_items[0].quantity * sorted_items[0].price) / total_value
        top_3_pct = sum(item.quantity * item.price for item in sorted_items[:3]) / total_value
        
        flag = "low"
        if top_pos_pct > 0.4 or top_3_pct > 0.7:
            flag = "high"
        elif top_pos_pct > 0.2:
            flag = "medium"

        # 2. Performance (Mocked)
        portfolio_return = 0.12 # 12% mock return
        annualized_return = 0.10 # 10% mock annualized

        # 3. Observations (Max 2-3)
        observations = []
        if flag == "high":
            observations.append({"severity": "warning", "text": "A large portion of your money is in a few stocks. Diversifying could lower your risk."})
        else:
            observations.append({"severity": "info", "text": "Your portfolio is well-spread across different investments!"})

        if portfolio_return > self.BENCHMARK_RETURN:
            observations.append({"severity": "info", "text": f"Great job! You are beating the market by {(portfolio_return - self.BENCHMARK_RETURN)*100:.1f}%."})

        # 4. Construct Final JSON
        response_json = {
            "concentration_risk": {
                "top_position_pct": round(top_pos_pct, 4),
                "top_3_positions_pct": round(top_3_pct, 4),
                "flag": flag
            },
            "performance": {
                "total_return_pct": portfolio_return,
                "annualized_return_pct": annualized_return
            },
            "benchmark_comparison": {
                "benchmark": "S&P 500",
                "portfolio_return_pct": portfolio_return,
                "benchmark_return_pct": self.BENCHMARK_RETURN,
                "alpha_pct": round(portfolio_return - self.BENCHMARK_RETURN, 4)
            },
            "observations": observations[:3],
            "disclaimer": "This is for educational purposes only and is not financial advice."
        }

        return AgentResponse(
            content=json.dumps(response_json),
            metadata={
                "total_value": total_value,
                "flag": flag
            }
        )

# Singleton
portfolio_health_agent = PortfolioHealthAgent()
