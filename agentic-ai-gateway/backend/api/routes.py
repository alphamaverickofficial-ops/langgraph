from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
import logging

from models.schemas import (
    # Requests
    ComplianceScanRequest,
    ContractAnalysisRequest,
    DataClassificationRequest,
    InfrastructureMonitorRequest,
    RiskAssessmentRequest,
    CodeReviewRequest,
    APISecurityScanRequest,
    DebugAnalysisRequest,
    TestGenerationRequest,
    # Responses
    ComplianceScanResponse,
    ContractAnalysisResponse,
    DataClassificationResponse,
    InfrastructureMonitorResponse,
    RiskAssessmentResponse,
    CodeReviewResponse,
    APISecurityScanResponse,
    DebugAnalysisResponse,
    TestGenerationResponse,
    GatewayStatusResponse,
    ServiceStatus,
)
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter()


# Service instances (will be imported from respective modules)
def get_service_instances():
    """Lazy load service instances to avoid circular imports."""
    services = {}
    try:
        from services.autocompliance_inspector.service import AutoComplianceInspectorService
        services["compliance"] = AutoComplianceInspectorService()
    except Exception as e:
        logger.warning(f"Could not load compliance service: {e}")
    
    try:
        from services.smart_contract_analyzer.service import SmartContractAnalyzerService
        services["contract"] = SmartContractAnalyzerService()
    except Exception as e:
        logger.warning(f"Could not load contract analyzer service: {e}")
    
    return services


@router.get("/status", response_model=GatewayStatusResponse)
async def get_gateway_status():
    """Get overall gateway and service status."""
    services = get_service_instances()
    service_statuses = []
    
    for name, service in services.items():
        try:
            health = await service.health_check()
            service_statuses.append(ServiceStatus(
                service_name=name,
                status=health.get("status", "unknown"),
                last_check=datetime.utcnow(),
                health_score=1.0 if health.get("status") == "healthy" else 0.5
            ))
        except Exception as e:
            logger.error(f"Health check failed for {name}: {e}")
            service_statuses.append(ServiceStatus(
                service_name=name,
                status="unhealthy",
                last_check=datetime.utcnow(),
                health_score=0.0
            ))
    
    return GatewayStatusResponse(
        success=True,
        message="Gateway status retrieved successfully",
        services=service_statuses,
        total_requests_today=0,
        average_response_time=0.0
    )


# Compliance Inspector Endpoint
@router.post("/compliance/scan", response_model=ComplianceScanResponse)
async def scan_compliance(request: ComplianceScanRequest):
    """Scan codebase for regulatory compliance violations."""
    services = get_service_instances()
    
    if "compliance" not in services:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Compliance service unavailable"
        )
    
    try:
        result = await services["compliance"].execute(request.model_dump())
        return ComplianceScanResponse(**result)
    except Exception as e:
        logger.error(f"Compliance scan failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Compliance scan failed: {str(e)}"
        )


# Smart Contract Analyzer Endpoint
@router.post("/contract/analyze", response_model=ContractAnalysisResponse)
async def analyze_contract(request: ContractAnalysisRequest):
    """Analyze smart contract for vulnerabilities and optimizations."""
    services = get_service_instances()
    
    if "contract" not in services:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Contract analyzer service unavailable"
        )
    
    try:
        result = await services["contract"].execute(request.model_dump())
        return ContractAnalysisResponse(**result)
    except Exception as e:
        logger.error(f"Contract analysis failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Contract analysis failed: {str(e)}"
        )


# Placeholder endpoints for remaining services
@router.post("/governance/classify")
async def classify_data(request: DataClassificationRequest):
    """Classify and tag sensitive data."""
    return {"success": True, "message": "Data governance service - Coming soon"}


@router.get("/infrastructure/monitor")
async def monitor_infrastructure(request: InfrastructureMonitorRequest):
    """Monitor cloud infrastructure and predict failures."""
    return {"success": True, "message": "Infrastructure monitoring service - Coming soon"}


@router.post("/risk/evaluate")
async def evaluate_risk(request: RiskAssessmentRequest):
    """Evaluate financial risk scores."""
    return {"success": True, "message": "Risk assessment service - Coming soon"}


@router.post("/review/pr")
async def review_pr(request: CodeReviewRequest):
    """Review pull requests intelligently."""
    return {"success": True, "message": "Code review service - Coming soon"}


@router.post("/security/scan")
async def scan_api_security(request: APISecurityScanRequest):
    """Scan APIs for security vulnerabilities."""
    return {"success": True, "message": "API security service - Coming soon"}


@router.post("/debug/analyze")
async def analyze_debug(request: DebugAnalysisRequest):
    """Analyze errors and suggest fixes."""
    return {"success": True, "message": "Debugging assistant service - Coming soon"}


@router.post("/tests/generate")
async def generate_tests(request: TestGenerationRequest):
    """Generate test cases from requirements."""
    return {"success": True, "message": "Test generation service - Coming soon"}
