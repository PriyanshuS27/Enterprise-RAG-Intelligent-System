"""
Enhanced RBAC System with Smart Features from Qlik Approach
- Conversation history
- Environment management (prod/dev)
- Permission caching
- Detailed metadata responses
- Tool-based organization
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum
import json
import hashlib
import time


# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================

class Environment(Enum):
    """System environments"""
    PROD = "prod"
    DEV = "dev"


class SecurityLevel(Enum):
    """Data security classification"""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class ConversationMessage:
    """Single message in conversation history"""
    timestamp: str
    user_id: str
    message_type: str  # 'user' or 'assistant'
    content: str
    metadata: Dict = field(default_factory=dict)


@dataclass
class ConversationSession:
    """User conversation session with history"""
    session_id: str
    user_id: str
    environment: str  # 'prod' or 'dev'
    created_at: str
    last_accessed: str
    messages: List[ConversationMessage] = field(default_factory=list)
    context: Dict = field(default_factory=dict)  # Conversation context
    
    def add_message(self, msg_type: str, content: str, metadata: Dict = None):
        """Add message to conversation"""
        self.last_accessed = datetime.now().isoformat()
        message = ConversationMessage(
            timestamp=datetime.now().isoformat(),
            user_id=self.user_id,
            message_type=msg_type,
            content=content,
            metadata=metadata or {}
        )
        self.messages.append(message)
    
    def get_conversation_context(self, limit: int = 5) -> str:
        """Get recent messages for context (for follow-up queries)"""
        recent = self.messages[-limit:]
        context_str = "\n".join([
            f"{m.timestamp} [{m.message_type.upper()}]: {m.content[:100]}..."
            for m in recent
        ])
        return context_str


@dataclass
class AccessRequest:
    """RBAC access request with metadata"""
    request_id: str
    user_id: str
    action: str  # 'read', 'write', 'delete', etc.
    resource: str
    environment: str
    timestamp: str
    status: str  # 'granted', 'denied', 'pending'
    reason: str
    metadata: Dict = field(default_factory=dict)


@dataclass
class EnhancedRAGResponse:
    """Enhanced response with rich metadata"""
    answer: str
    sources: List[str]
    confidence: float
    user: str
    role: str
    environment: str  # Which environment (prod/dev)
    access_granted: bool
    timestamp: str
    
    # Enhanced metadata
    access_request: AccessRequest
    conversation_id: Optional[str] = None
    follow_up_possible: bool = True
    
    audit_log: Dict = field(default_factory=dict)
    
    def to_json(self) -> str:
        """Convert to JSON response"""
        return json.dumps({
            'answer': self.answer,
            'sources': self.sources,
            'confidence': self.confidence,
            'user': self.user,
            'role': self.role,
            'environment': self.environment,
            'access_granted': self.access_granted,
            'timestamp': self.timestamp,
            'conversation_id': self.conversation_id,
            'follow_up_possible': self.follow_up_possible,
            'access_request': asdict(self.access_request),
            'audit_log': self.audit_log
        }, indent=2)


# ============================================================================
# PERMISSION CACHING (Performance Optimization)
# ============================================================================

@dataclass
class CachedPermission:
    """Cached permission with expiry"""
    user_id: str
    role: str
    permissions: set
    environment: str
    cached_at: float
    expires_at: float  # unix timestamp
    
    def is_expired(self) -> bool:
        """Check if cache is expired"""
        return time.time() > self.expires_at


class PermissionCache:
    """Simple permission cache to reduce API calls"""
    
    def __init__(self, ttl_seconds: int = 300):  # 5 min default
        self.cache: Dict[str, CachedPermission] = {}
        self.ttl = ttl_seconds
    
    def get(self, user_id: str, environment: str) -> Optional[set]:
        """Get cached permissions"""
        key = f"{user_id}:{environment}"
        if key in self.cache:
            cached = self.cache[key]
            if not cached.is_expired():
                return cached.permissions
            else:
                del self.cache[key]  # Remove expired
        return None
    
    def set(self, user_id: str, role: str, permissions: set, environment: str):
        """Cache permissions"""
        key = f"{user_id}:{environment}"
        self.cache[key] = CachedPermission(
            user_id=user_id,
            role=role,
            permissions=permissions,
            environment=environment,
            cached_at=time.time(),
            expires_at=time.time() + self.ttl
        )
    
    def clear(self):
        """Clear entire cache"""
        self.cache.clear()


# ============================================================================
# CONVERSATION MANAGER
# ============================================================================

class ConversationManager:
    """Manage user conversation sessions"""
    
    def __init__(self):
        self.sessions: Dict[str, ConversationSession] = {}
    
    def create_session(self, user_id: str, environment: str = "prod") -> ConversationSession:
        """Create new conversation session"""
        session_id = hashlib.md5(
            f"{user_id}:{datetime.now().isoformat()}".encode()
        ).hexdigest()
        
        session = ConversationSession(
            session_id=session_id,
            user_id=user_id,
            environment=environment,
            created_at=datetime.now().isoformat(),
            last_accessed=datetime.now().isoformat()
        )
        self.sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        """Get existing session"""
        return self.sessions.get(session_id)
    
    def add_message(self, session_id: str, msg_type: str, content: str, metadata: Dict = None):
        """Add message to session"""
        session = self.get_session(session_id)
        if session:
            session.add_message(msg_type, content, metadata)
    
    def get_session_for_user(self, user_id: str, environment: str = "prod") -> ConversationSession:
        """Get or create session for user"""
        for session in self.sessions.values():
            if session.user_id == user_id and session.environment == environment:
                return session
        return self.create_session(user_id, environment)
    
    def cleanup_old_sessions(self, hours: int = 24):
        """Remove sessions older than X hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        to_delete = []
        
        for session_id, session in self.sessions.items():
            last_accessed = datetime.fromisoformat(session.last_accessed)
            if last_accessed < cutoff_time:
                to_delete.append(session_id)
        
        for session_id in to_delete:
            del self.sessions[session_id]


# ============================================================================
# TOOL-BASED RBAC FUNCTIONS (Organized like Qlik)
# ============================================================================

class RBACTools:
    """Organized RBAC tools/functions"""
    
    def __init__(self, rbac_enforcer, conversation_manager, permission_cache):
        """Initialize tools with dependencies"""
        self.rbac = rbac_enforcer
        self.conv_manager = conversation_manager
        self.perm_cache = permission_cache
    
    def check_access(
        self,
        user_id: str,
        action: str,
        resource: str,
        environment: str = "prod",
        session_id: Optional[str] = None
    ) -> AccessRequest:
        """
        Check if user has access to resource for given action
        Returns: AccessRequest with detailed metadata
        """
        request_id = hashlib.md5(
            f"{user_id}:{action}:{resource}:{datetime.now().isoformat()}".encode()
        ).hexdigest()
        
        user = self.rbac.USERS.get(user_id)
        if not user:
            return AccessRequest(
                request_id=request_id,
                user_id=user_id,
                action=action,
                resource=resource,
                environment=environment,
                timestamp=datetime.now().isoformat(),
                status="denied",
                reason=f"User {user_id} not found",
                metadata={"error": "user_not_found"}
            )
        
        # Check cached permissions first
        cached_perms = self.perm_cache.get(user_id, environment)
        
        if cached_perms:
            has_access = action in cached_perms
            status = "granted" if has_access else "denied"
        else:
            # Get permissions dynamically
            perms = self.rbac.get_permissions(user.role, environment)
            self.perm_cache.set(user_id, user.role, perms, environment)
            has_access = action in perms
            status = "granted" if has_access else "denied"
        
        # Add to conversation history if session exists
        if session_id:
            metadata = {
                "action": action,
                "resource": resource,
                "environment": environment
            }
            self.conv_manager.add_message(
                session_id,
                "access_check",
                f"{action} on {resource}",
                metadata
            )
        
        return AccessRequest(
            request_id=request_id,
            user_id=user_id,
            action=action,
            resource=resource,
            environment=environment,
            timestamp=datetime.now().isoformat(),
            status=status,
            reason=f"User role '{user.role}' {'has' if has_access else 'does not have'} permission for {action}",
            metadata={
                "user_role": user.role,
                "user_department": user.department,
                "cached": cached_perms is not None
            }
        )
    
    def get_user_info(self, user_id: str) -> Dict:
        """Get detailed user information"""
        user = self.rbac.USERS.get(user_id)
        if not user:
            return {"error": "User not found", "user_id": user_id}
        
        return {
            "user_id": user.user_id,
            "name": user.name,
            "role": user.role,
            "department": user.department,
            "permissions_prod": list(self.rbac.get_permissions(user.role, "prod")),
            "permissions_dev": list(self.rbac.get_permissions(user.role, "dev"))
        }
    
    def get_all_users(self) -> List[Dict]:
        """List all users with metadata"""
        return [self.get_user_info(uid) for uid in self.rbac.USERS.keys()]


# ============================================================================
# AUDIT TRAIL ENHANCEMENT
# ============================================================================

class AuditTrail:
    """Enhanced audit trail with detailed logging"""
    
    def __init__(self):
        self.logs: List[Dict] = []
    
    def log_access(self, access_request: AccessRequest, answer_snippet: str = ""):
        """Log an access request"""
        self.logs.append({
            "request_id": access_request.request_id,
            "timestamp": access_request.timestamp,
            "user_id": access_request.user_id,
            "action": access_request.action,
            "resource": access_request.resource,
            "environment": access_request.environment,
            "status": access_request.status,
            "reason": access_request.reason,
            "answer_snippet": answer_snippet[:50] + "..." if answer_snippet else "",
            "metadata": access_request.metadata
        })
    
    def get_audit_logs(self, user_id: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """Get audit logs, optionally filtered by user"""
        logs = self.logs
        if user_id:
            logs = [l for l in logs if l["user_id"] == user_id]
        return logs[-limit:]
    
    def export_audit_logs(self, filepath: str):
        """Export audit logs to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.logs, f, indent=2)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def normalize_action(action: str) -> str:
    """Normalize action names (similar to Qlik approach)"""
    action_map = {
        "read": ["read", "view", "access", "query"],
        "write": ["write", "create", "add", "modify"],
        "delete": ["delete", "remove", "drop"],
        "publish": ["publish", "share", "deploy"],
        "admin": ["admin", "manage", "configure"]
    }
    
    action_lower = action.lower().strip()
    for canonical, synonyms in action_map.items():
        if action_lower in synonyms:
            return canonical
    return action_lower


def normalize_environment(env: Optional[str]) -> str:
    """Normalize environment name"""
    if not env:
        return "prod"
    env_lower = env.lower().strip()
    env_map = {
        "prod": ["prod", "production", "prod-env"],
        "dev": ["dev", "development", "dev-env", "development-env"]
    }
    for canonical, synonyms in env_map.items():
        if env_lower in synonyms:
            return canonical
    return "prod"
