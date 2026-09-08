from typing import Dict, Any, List
import logging
from datetime import datetime
import re
import sys

# Add parent path for imports
sys.path.insert(0, '/workspace/agentic-ai-gateway/backend')
from services.base_service import BaseAIService

logger = logging.getLogger(__name__)


class SmartContractAnalyzerService(BaseAIService):
    """
    AI-powered smart contract auditing tool.
    Identifies security vulnerabilities, gas optimization opportunities,
    and compliance issues in blockchain contracts.
    """
    
    VULNERABILITY_PATTERNS = {
        "reentrancy": {
            "pattern": r"(call|delegatecall|staticcall)\s*\([^)]*\)\s*;",
            "severity": "critical",
            "description": "Potential reentrancy vulnerability detected"
        },
        "integer_overflow": {
            "pattern": r"(\+\+|--|\+=|-=)[^;]*;",
            "severity": "high",
            "description": "Potential integer overflow/underflow"
        },
        "unchecked_return": {
            "pattern": r"(?!require|assert).*\.transfer\(",
            "severity": "medium",
            "description": "Unchecked transfer return value"
        },
        "tx_origin_auth": {
            "pattern": r"tx\.origin",
            "severity": "high",
            "description": "Use of tx.origin for authentication"
        },
        "weak_randomness": {
            "pattern": r"(block\.timestamp|now|block\.number)",
            "severity": "medium",
            "description": "Potentially weak randomness source"
        }
    }
    
    GAS_OPTIMIZATIONS = [
        {
            "name": "Use calldata instead of memory",
            "description": "Function parameters can use calldata to save gas",
            "potential_savings": 2000
        },
        {
            "name": "Cache array length",
            "description": "Store array.length in a variable for loops",
            "potential_savings": 100
        },
        {
            "name": "Use ++i instead of i++",
            "description": "Pre-increment is slightly cheaper than post-increment",
            "potential_savings": 5
        },
        {
            "name": "Short-circuit boolean expressions",
            "description": "Order conditions by likelihood and cost",
            "potential_savings": 500
        }
    ]
    
    def __init__(self):
        super().__init__("SmartContractAnalyzer")
    
    async def execute(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze smart contract for vulnerabilities."""
        start_time = datetime.utcnow()
        
        contract_code = request_data.get("contract_code", "")
        contract_address = request_data.get("contract_address", "")
        blockchain = request_data.get("blockchain", "ethereum")
        
        self.log_request(request_data.get("request_id", "unknown"), request_data)
        
        # Analyze contract code
        vulnerabilities = await self._find_vulnerabilities(contract_code)
        gas_optimizations = await self._find_gas_optimizations(contract_code)
        compliance_issues = await self._check_compliance(contract_code, blockchain)
        
        response = {
            "success": True,
            "message": f"Smart contract analysis completed for {blockchain}",
            "analysis_id": self.generate_id("contract"),
            "vulnerabilities": vulnerabilities,
            "gas_optimizations": gas_optimizations,
            "compliance_issues": compliance_issues,
            "summary": {
                "total_vulnerabilities": len(vulnerabilities),
                "critical": len([v for v in vulnerabilities if v["severity"] == "critical"]),
                "high": len([v for v in vulnerabilities if v["severity"] == "high"]),
                "medium": len([v for v in vulnerabilities if v["severity"] == "medium"]),
                "low": len([v for v in vulnerabilities if v["severity"] == "low"]),
                "total_gas_savings_potential": sum(opt.get("potential_savings", 0) for opt in gas_optimizations)
            }
        }
        
        duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
        self.log_response(request_data.get("request_id", "unknown"), True, duration_ms)
        
        return response
    
    async def _find_vulnerabilities(self, code: str) -> List[Dict[str, Any]]:
        """Find security vulnerabilities in contract code."""
        vulnerabilities = []
        
        for vuln_type, vuln_info in self.VULNERABILITY_PATTERNS.items():
            matches = re.finditer(vuln_info["pattern"], code, re.MULTILINE)
            for match in matches:
                line_number = code[:match.start()].count('\n') + 1
                vulnerabilities.append({
                    "type": vuln_type,
                    "severity": vuln_info["severity"],
                    "description": vuln_info["description"],
                    "line_number": line_number,
                    "gas_impact": None
                })
        
        return vulnerabilities
    
    async def _find_gas_optimizations(self, code: str) -> List[Dict[str, Any]]:
        """Identify gas optimization opportunities."""
        optimizations = []
        
        # Simple pattern matching for demo
        if "memory" in code and "function" in code:
            optimizations.append(self.GAS_OPTIMIZATIONS[0])
        
        if ".length" in code and "for" in code:
            optimizations.append(self.GAS_OPTIMIZATIONS[1])
        
        if "i++" in code:
            optimizations.append(self.GAS_OPTIMIZATIONS[2])
        
        return optimizations
    
    async def _check_compliance(self, code: str, blockchain: str) -> List[Dict[str, Any]]:
        """Check compliance with blockchain-specific standards."""
        compliance_issues = []
        
        # ERC20 compliance check
        if blockchain == "ethereum":
            required_functions = ["transfer", "approve", "balanceOf", "totalSupply"]
            for func in required_functions:
                if func not in code:
                    compliance_issues.append({
                        "standard": "ERC20",
                        "issue": f"Missing required function: {func}",
                        "severity": "high"
                    })
        
        return compliance_issues
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for smart contract analyzer."""
        return {
            "service": self.service_name,
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "supported_blockchains": ["ethereum", "polygon", "bsc", "arbitrum"]
        }
