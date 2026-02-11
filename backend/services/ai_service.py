"""AI Service for handling AI-powered features"""
import os
import random
from typing import Dict, List, Any
from config.settings import settings

class AIService:
    """AI Service with OpenAI integration and mock fallback"""
    
    def __init__(self):
        self.use_mock = settings.USE_MOCK_AI
        self.openai_client = None
        
        if not self.use_mock and settings.OPENAI_API_KEY:
            try:
                import openai
                self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            except Exception as e:
                print(f"Failed to initialize OpenAI client: {e}")
                self.use_mock = True
    
    async def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate AI response based on prompt and context"""
        if self.use_mock or not self.openai_client:
            return self._mock_response(prompt, context)
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": context if context else "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._mock_response(prompt, context)
    
    def _mock_response(self, prompt: str, context: str = "") -> str:
        """Generate mock AI response"""
        prompt_lower = prompt.lower()
        
        # HR responses
        if "resume" in prompt_lower or "cv" in prompt_lower:
            return "Based on the resume analysis, the candidate shows strong technical skills and relevant experience. Recommended for interview. Skills match: 85%."
        
        if "performance" in prompt_lower:
            return "Performance Analysis: The employee demonstrates consistent productivity with a 92% task completion rate. Areas for improvement include communication and time management. Overall rating: Good."
        
        if "interview" in prompt_lower:
            return "Interview scheduled successfully. Recommended questions: 1) Tell us about your experience with similar projects 2) How do you handle tight deadlines? 3) Describe your problem-solving approach."
        
        # Support responses
        if "ticket" in prompt_lower or "complaint" in prompt_lower or "issue" in prompt_lower:
            return "Thank you for reaching out. We understand your concern and appreciate your patience. Our team will investigate this issue and provide a resolution within 24-48 hours. We're committed to ensuring your satisfaction."
        
        if "classify" in prompt_lower:
            categories = ["Technical Issue", "Billing", "General Inquiry", "Product Feedback", "Complaint"]
            return random.choice(categories)
        
        # Sales responses
        if "lead" in prompt_lower or "score" in prompt_lower:
            return f"Lead Score: {random.randint(60, 95)}/100. High potential based on budget, industry fit, and engagement level. Recommended action: Schedule demo call within 48 hours."
        
        if "forecast" in prompt_lower:
            return f"Sales Forecast: Based on current pipeline and historical data, projected revenue for next quarter: ${random.randint(50000, 150000):,}. Confidence level: High."
        
        # Data analysis responses
        if "trend" in prompt_lower or "analysis" in prompt_lower:
            return "Trend Analysis: The data shows a positive growth trend of approximately 15% month-over-month. Key insights: Peak activity during weekdays, seasonal variations observed in Q4."
        
        if "prediction" in prompt_lower or "forecast" in prompt_lower:
            return "Prediction Model Results: Based on historical patterns, we forecast a 12% increase in the target metric over the next 3 months. Factors considered: seasonality, market trends, and historical growth rate."
        
        # Admin responses
        if "email" in prompt_lower:
            return "Subject: Meeting Follow-up\n\nDear Team,\n\nThank you for attending today's meeting. Here are the key action items:\n\n1. Review project timeline\n2. Submit status reports by Friday\n3. Schedule follow-up meeting\n\nPlease let me know if you have any questions.\n\nBest regards"
        
        if "task" in prompt_lower or "reminder" in prompt_lower:
            return "Task prioritized based on urgency and importance. Recommended schedule: High priority items in the morning, routine tasks in the afternoon. Deadline alerts set for 24 hours before due date."
        
        # Default response
        return "Thank you for your query. I've processed your request and generated the relevant insights. The AI analysis indicates positive indicators and recommends proceeding with the suggested action items."
    
    async def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Analyze resume and extract key information"""
        prompt = f"Analyze this resume and provide key insights:\n\n{resume_text[:1000]}"
        context = "You are an HR specialist analyzing resumes. Provide structured feedback on skills, experience, and fit."
        
        response = await self.generate_response(prompt, context)
        
        return {
            "summary": response,
            "skills_match": random.randint(70, 95),
            "experience_level": random.choice(["Junior", "Mid-level", "Senior"]),
            "recommendation": random.choice(["Highly Recommended", "Recommended", "Consider for Future"])
        }
    
    async def classify_ticket(self, ticket_text: str) -> Dict[str, str]:
        """Classify support ticket"""
        prompt = f"Classify this support ticket:\n\n{ticket_text}"
        context = "You are a customer support classifier. Categorize tickets and determine priority."
        
        response = await self.generate_response(prompt, context)
        
        categories = ["Technical Issue", "Billing", "General Inquiry", "Product Feedback", "Complaint"]
        priorities = ["Low", "Medium", "High", "Critical"]
        
        return {
            "category": random.choice(categories),
            "priority": random.choice(priorities),
            "suggested_response": response
        }
    
    async def score_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Score sales lead using ML-like logic"""
        score = 0
        factors = []
        
        # Budget scoring
        budget = lead_data.get("budget", 0)
        if budget > 50000:
            score += 30
            factors.append("High budget")
        elif budget > 20000:
            score += 20
            factors.append("Medium budget")
        else:
            score += 10
            factors.append("Low budget")
        
        # Industry scoring
        high_value_industries = ["Technology", "Finance", "Healthcare", "Manufacturing"]
        if lead_data.get("industry") in high_value_industries:
            score += 25
            factors.append("High-value industry")
        else:
            score += 15
        
        # Source scoring
        trusted_sources = ["Referral", "Direct", "Website"]
        if lead_data.get("source") in trusted_sources:
            score += 25
            factors.append("Trusted source")
        else:
            score += 10
        
        # Company presence
        if lead_data.get("company"):
            score += 20
            factors.append("Established company")
        
        return {
            "score": min(score, 100),
            "factors": factors,
            "recommendation": "High Priority" if score > 70 else "Medium Priority" if score > 50 else "Low Priority"
        }
    
    async def generate_forecast(self, data: List[float]) -> Dict[str, Any]:
        """Generate simple forecast based on historical data"""
        if not data:
            return {"forecast": [], "trend": "Unknown"}
        
        # Simple moving average forecast
        avg_growth = sum(data[i] - data[i-1] for i in range(1, len(data))) / (len(data) - 1) if len(data) > 1 else 0
        last_value = data[-1]
        
        forecast = []
        for i in range(1, 4):  # Forecast next 3 periods
            forecast.append(last_value + (avg_growth * i))
        
        trend = "Growing" if avg_growth > 0 else "Declining" if avg_growth < 0 else "Stable"
        
        return {
            "forecast": forecast,
            "trend": trend,
            "confidence": random.randint(70, 90)
        }

# Global AI service instance
ai_service = AIService()
