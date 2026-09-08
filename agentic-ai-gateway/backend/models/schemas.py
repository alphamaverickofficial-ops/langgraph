from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ScanStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# Base request/response models
class BaseRequest(BaseModel):
    """Base request model with common fields."""
    request_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class BaseResponse(BaseModel):
    """Base response model with common fields."""
    success: bool
    message: str
    request_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Compliance models
class ComplianceScanRequest(BaseRequest):
    codebase_path: str
    regulations: List[str] = ["SOX", "PCI-DSS"]
    generate_audit_trail: bool = True


class ComplianceViolation(BaseModel):
    regulation: str
    severity: RiskLevel
    description: str
    location: str
    remediation: str


class ComplianceScanResponse(BaseResponse):
    scan_id: str
    status: ScanStatus
    violations: List[ComplianceViolation] = []
    audit_trail_url: Optional[str] = None
    summary: Dict[str, Any] = {}


# Smart Contract models
class ContractAnalysisRequest(BaseRequest):
    contract_address: Optional[str] = None
    contract_code: Optional[str] = None
    blockchain: str = "ethereum"


class Vulnerability(BaseModel):
    type: str
    severity: RiskLevel
    description: str
    line_number: Optional[int] = None
    gas_impact: Optional[int] = None


class ContractAnalysisResponse(BaseResponse):
    analysis_id: str
    vulnerabilities: List[Vulnerability] = []
    gas_optimizations: List[Dict[str, Any]] = []
    compliance_issues: List[Dict[str, Any]] = []


# Data Governance models
class DataClassificationRequest(BaseRequest):
    data_source: str
    data_sample: str
    classification_rules: Optional[List[str]] = None


class DataTag(BaseModel):
    tag_name: str
    confidence: float
    category: str


class DataClassificationResponse(BaseResponse):
    classification_id: str
    tags: List[DataTag] = []
    sensitivity_level: RiskLevel
    gdpr_compliant: bool
    ccpa_compliant: bool
    lineage: List[Dict[str, Any]] = []


# Infrastructure models
class InfrastructureMonitorRequest(BaseRequest):
    cloud_provider: str = "aws"
    resource_ids: Optional[List[str]] = None
    prediction_window: int = 24  # hours


class InfrastructureAlert(BaseModel):
    resource_id: str
    alert_type: str
    predicted_failure_time: Optional[datetime] = None
    confidence: float
    recommended_action: str


class InfrastructureMonitorResponse(BaseResponse):
    monitor_id: str
    alerts: List[InfrastructureAlert] = []
    health_score: float
    scaling_recommendations: List[Dict[str, Any]] = []


# Risk Assessment models
class RiskAssessmentRequest(BaseRequest):
    portfolio_data: Dict[str, Any]
    market_data: Optional[Dict[str, Any]] = None
    transaction_history: Optional[List[Dict[str, Any]]] = None


class RiskAssessmentResponse(BaseResponse):
    assessment_id: str
    risk_score: float
    risk_level: RiskLevel
    risk_factors: List[Dict[str, Any]] = []
    mitigation_recommendations: List[str] = []


# Code Review models
class CodeReviewRequest(BaseRequest):
    pr_url: Optional[str] = None
    code_diff: Optional[str] = None
    repository: str
    business_context: Optional[str] = None


class CodeReviewComment(BaseModel):
    file_path: str
    line_number: int
    comment_type: str
    message: str
    suggestion: Optional[str] = None


class CodeReviewResponse(BaseResponse):
    review_id: str
    comments: List[CodeReviewComment] = []
    security_issues: int = 0
    performance_issues: int = 0
    standards_violations: int = 0
    overall_quality: float


# API Security models
class APISecurityScanRequest(BaseRequest):
    api_spec_url: Optional[str] = None
    api_spec_content: Optional[str] = None
    endpoints: Optional[List[str]] = None
    scan_depth: str = "full"


class APIVulnerability(BaseModel):
    endpoint: str
    vulnerability_type: str
    owasp_category: str
    severity: RiskLevel
    cwe_id: Optional[str] = None
    patch_suggestion: Optional[str] = None


class APISecurityScanResponse(BaseResponse):
    scan_id: str
    vulnerabilities: List[APIVulnerability] = []
    secure_patches: List[Dict[str, Any]] = []
    security_score: float


# Debugging models
class DebugAnalysisRequest(BaseRequest):
    error_logs: str
    stack_trace: Optional[str] = None
    system_metrics: Optional[Dict[str, Any]] = None
    code_snippet: Optional[str] = None


class DebugSuggestion(BaseModel):
    root_cause: str
    fix_description: str
    code_fix: Optional[str] = None
    confidence: float


class DebugAnalysisResponse(BaseResponse):
    analysis_id: str
    suggestions: List[DebugSuggestion] = []
    reproduction_steps: Optional[List[str]] = None


# Test Generation models
class TestGenerationRequest(BaseRequest):
    requirements_doc: str
    codebase_path: Optional[str] = None
    test_framework: str = "pytest"
    coverage_target: float = 80.0


class TestCase(BaseModel):
    test_name: str
    test_description: str
    test_code: str
    test_type: str
    edge_case: bool = False


class TestGenerationResponse(BaseResponse):
    generation_id: str
    test_cases: List[TestCase] = []
    coverage_metrics: Dict[str, float] = {}
    edge_cases_count: int = 0


# Unified Gateway models
class ServiceStatus(BaseModel):
    service_name: str
    status: str
    last_check: datetime
    health_score: float


class GatewayStatusResponse(BaseResponse):
    services: List[ServiceStatus] = []
    total_requests_today: int = 0
    average_response_time: float = 0.0
