"""
Resource Configuration System
Defines resource types, keywords, and document mappings
This is a flexible, data-driven approach (NOT hard-coded)
"""

# ============================================================================
# RESOURCE DEFINITIONS
# ============================================================================
# This is a single source of truth for all resources in the system
RESOURCE_MAPPING = {
    "patient": {
        "keywords": ["patient", "medical", "condition", "treatment", "lab result", "diagnosis", "hospital", "medical record"],
        "required_documents": ["CSV_001"],  # patients.csv
        "roles_allowed": ["doctor", "admin"],
        "security_level": "restricted",
        "description": "Patient medical records and health information"
    },
    
    "employee": {
        "keywords": ["employee", "salary", "payroll", "hr data", "department", "designation"],
        "required_documents": ["CSV_002"],  # employees.csv
        "roles_allowed": ["hr", "admin"],
        "security_level": "confidential",
        "description": "Employee information and salary data"
    },
    
    "appointments": {
        "keywords": ["appointment", "schedule", "booking", "slot", "timing"],
        "required_documents": ["CSV_003"],  # appointments.csv
        "roles_allowed": ["doctor", "hr", "admin"],
        "security_level": "internal",
        "description": "Appointment and scheduling information"
    },
    
    "audit": {
        "keywords": ["audit log", "audit trail", "system event", "access log", "activity"],
        "required_documents": ["JSON_001"],  # audit_logs.json
        "roles_allowed": ["admin", "engineer"],
        "security_level": "confidential",
        "description": "Audit trails and system activity logs"
    },
    
    "alerts": {
        "keywords": ["alert", "system alert", "notification", "warning", "status"],
        "required_documents": ["JSON_002"],  # alerts.json
        "roles_allowed": ["admin", "engineer"],
        "security_level": "internal",
        "description": "System alerts and notifications"
    },
    
    "compliance": {
        "keywords": ["compliance", "gdpr", "hipaa", "regulation", "policy"],
        "required_documents": ["JSON_003"],  # compliance.json
        "roles_allowed": ["admin", "hr"],
        "security_level": "confidential",
        "description": "Compliance and regulatory information"
    },
    
    "finance": {
        "keywords": ["transaction", "financial", "payment", "amount", "budget", "expense"],
        "required_documents": ["SQL_002"],  # transactions
        "roles_allowed": ["admin"],
        "security_level": "confidential",
        "description": "Financial transactions and payments"
    },
    
    "labresults": {
        "keywords": ["lab result", "test result", "lab test", "blood test", "report"],
        "required_documents": ["SQL_001"],  # lab_results
        "roles_allowed": ["doctor", "admin"],
        "security_level": "restricted",
        "description": "Laboratory test results and medical reports"
    }
}


# ============================================================================
# RESOURCE MANAGEMENT FUNCTIONS
# ============================================================================

def detect_requested_resources(query: str) -> list:
    """
    Detect which resources are being requested in a query
    Args: query (str) - User's query
    Returns: list of resource names
    """
    query_lower = query.lower()
    requested = []
    
    for resource, config in RESOURCE_MAPPING.items():
        keywords = config["keywords"]
        if any(kw in query_lower for kw in keywords):
            requested.append(resource)
    
    return requested


def get_required_documents(resource: str) -> list:
    """
    Get document IDs required to access a resource
    Args: resource (str) - Resource name
    Returns: list of document IDs
    """
    if resource in RESOURCE_MAPPING:
        return RESOURCE_MAPPING[resource]["required_documents"]
    return []


def get_allowed_roles(resource: str) -> list:
    """
    Get roles that can access a resource
    Args: resource (str) - Resource name
    Returns: list of role names
    """
    if resource in RESOURCE_MAPPING:
        return RESOURCE_MAPPING[resource]["roles_allowed"]
    return []


def check_resource_access(user_role: str, resource: str) -> bool:
    """
    Check if a user role can access a resource
    Args: user_role (str), resource (str)
    Returns: bool - True if access allowed
    """
    allowed_roles = get_allowed_roles(resource)
    return user_role in allowed_roles


def get_resource_info(resource: str) -> dict:
    """
    Get complete information about a resource
    Args: resource (str)
    Returns: dict with resource configuration
    """
    return RESOURCE_MAPPING.get(resource, {})


# ============================================================================
# AUDIT LOG FUNCTIONS
# ============================================================================

def log_access_attempt(user_id: str, resource: str, allowed: bool, reason: str = "") -> dict:
    """
    Log a resource access attempt
    """
    return {
        "user_id": user_id,
        "resource": resource,
        "allowed": allowed,
        "reason": reason,
        "resource_description": RESOURCE_MAPPING.get(resource, {}).get("description", "Unknown"),
        "security_level": RESOURCE_MAPPING.get(resource, {}).get("security_level", "unknown")
    }
