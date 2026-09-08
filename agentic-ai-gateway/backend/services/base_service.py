from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class BaseAIService(ABC):
    """Base class for all AI services in the gateway."""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{service_name}")
    
    @abstractmethod
    async def execute(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the service logic."""
        pass
    
    def generate_id(self, prefix: str) -> str:
        """Generate a unique ID for requests."""
        return f"{prefix}_{uuid.uuid4().hex[:12]}"
    
    def log_request(self, request_id: str, data: Dict[str, Any]):
        """Log incoming request."""
        self.logger.info(f"Request {request_id} received for {self.service_name}")
    
    def log_response(self, request_id: str, success: bool, duration_ms: float):
        """Log outgoing response."""
        status = "success" if success else "failed"
        self.logger.info(f"Request {request_id} {status} in {duration_ms:.2f}ms")
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check for the service."""
        return {
            "service": self.service_name,
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat()
        }
