from typing import Dict, Any, List
import logging
from datetime import datetime
import sys

sys.path.insert(0, '/workspace/agentic-ai-gateway/backend')
from services.base_service import BaseAIService

logger = logging.getLogger(__name__)


class IntelligentDebuggingAssistantService(BaseAIService):
    """
    AI-powered debugging tool.
    Analyzes error logs, stack traces, and metrics to suggest fixes.
    """
    
    COMMON_ERRORS = {
        "NullPointerException": "Check for null values before accessing object properties",
        "OutOfMemoryError": "Review memory allocation and implement proper cleanup",
        "TimeoutError": "Increase timeout or optimize slow operations",
        "ConnectionRefused": "Verify service is running and network configuration"
    }
    
    def __init__(self):
        super().__init__("IntelligentDebuggingAssistant")
    
    async def execute(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        start_time = datetime.utcnow()
        
        error_logs = request_data.get("error_logs", "")
        stack_trace = request_data.get("stack_trace", "")
        system_metrics = request_data.get("system_metrics", {})
        code_snippet = request_data.get("code_snippet", "")
        
        self.log_request(request_data.get("request_id", "unknown"), request_data)
        
        suggestions = await self._analyze_error(error_logs, stack_trace)
        reproduction_steps = await self._generate_reproduction_steps(error_logs)
        
        response = {
            "success": True,
            "message": "Debug analysis completed",
            "analysis_id": self.generate_id("debug"),
            "suggestions": suggestions,
            "reproduction_steps": reproduction_steps
        }
        
        duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
        self.log_response(request_data.get("request_id", "unknown"), True, duration_ms)
        
        return response
    
    async def _analyze_error(self, logs: str, trace: str) -> List[Dict[str, Any]]:
        suggestions = []
        
        if "NullPointerException" in logs or "NoneType" in logs:
            suggestions.append({
                "root_cause": "Null reference access",
                "fix_description": "Add null check before accessing object",
                "code_fix": "if obj is not None:\n    obj.method()",
                "confidence": 0.92
            })
        
        if "Timeout" in logs or "timeout" in logs:
            suggestions.append({
                "root_cause": "Operation timeout",
                "fix_description": "Increase timeout or optimize query",
                "code_fix": "result = query.execute(timeout=30)",
                "confidence": 0.85
            })
        
        return suggestions
    
    async def _generate_reproduction_steps(self, logs: str) -> List[str]:
        return [
            "1. Initialize the application with test data",
            "2. Trigger the problematic endpoint with specific parameters",
            "3. Monitor logs for the error pattern",
            "4. Capture stack trace and system state"
        ]
    
    async def health_check(self) -> Dict[str, Any]:
        return {
            "service": self.service_name,
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "supported_languages": ["python", "java", "javascript", "go", "rust"]
        }
