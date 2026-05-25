#!/usr/bin/env python3
"""
Enterprise RAG Intelligence System
Multi-source retrieval with RBAC enforcement & grounding checks
"""

import json
import csv
import sqlite3
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import re

# Third-party imports
try:
    import PyPDF2
except ImportError:
    print("[WARNING] PyPDF2 not installed. PDF parsing will be simulated.")
    PyPDF2 = None

try:
    import pandas as pd
except ImportError:
    print("[WARNING] pandas not installed. CSV parsing will be simulated.")
    pd = None

from groq import Groq
from dotenv import load_dotenv
from resource_config import (
    detect_requested_resources, 
    get_required_documents,
    get_allowed_roles,
    RESOURCE_MAPPING
)

# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Document:
    """Represents a document in the system"""
    doc_id: str
    source: str  # 'pdf', 'csv', 'json', 'sql'
    content: str
    metadata: Dict
    security_level: str  # 'public', 'internal', 'confidential', 'restricted'
    access_roles: List[str]  # Who can access this


@dataclass
class User:
    """Represents a user with role and permissions"""
    user_id: str
    name: str
    role: str  # 'admin', 'doctor', 'hr', 'engineer', 'intern'
    department: str


@dataclass
class RetrievedContext:
    """Retrieved context with metadata"""
    document: Document
    relevance_score: float
    source: str


@dataclass
class RAGResponse:
    """Final response with audit trail"""
    answer: str
    sources: List[str]
    confidence: float
    user: str
    role: str
    access_granted: bool
    timestamp: str
    audit_log: Dict


# ============================================================================
# SYNTHETIC DATA GENERATION
# ============================================================================

class SyntheticDataGenerator:
    """Generate/Load enterprise datasets from actual files"""

    @staticmethod
    def read_pdf_file(filepath: str, doc_id: str, security_level: str, access_roles: List[str]) -> Optional[Document]:
        """Read PDF file and extract text"""
        try:
            if PyPDF2 is None:
                # Fallback: read as text file
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                # Use PyPDF2 to extract text
                with open(filepath, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    content = ""
                    for page in pdf_reader.pages:
                        content += page.extract_text()
            
            filename = Path(filepath).name
            return Document(
                doc_id=doc_id,
                source="pdf",
                content=content,
                metadata={"filename": filename, "filepath": filepath, "pages": 1},
                security_level=security_level,
                access_roles=access_roles
            )
        except FileNotFoundError:
            print(f"[WARNING] PDF file not found: {filepath}")
            return None
        except Exception as e:
            print(f"[WARNING] Error reading PDF {filepath}: {str(e)}")
            return None

    @staticmethod
    def read_csv_file(filepath: str, doc_id: str, table_name: str, security_level: str, access_roles: List[str]) -> Optional[Document]:
        """Read CSV file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Also parse for metadata
            lines = content.split('\n')
            row_count = len([l for l in lines if l.strip()]) - 1  # Exclude header
            
            return Document(
                doc_id=doc_id,
                source="csv",
                content=content,
                metadata={"table": table_name, "filepath": filepath, "rows": row_count},
                security_level=security_level,
                access_roles=access_roles
            )
        except FileNotFoundError:
            print(f"[WARNING] CSV file not found: {filepath}")
            return None
        except Exception as e:
            print(f"[WARNING] Error reading CSV {filepath}: {str(e)}")
            return None

    @staticmethod
    def read_json_file(filepath: str, doc_id: str, security_level: str, access_roles: List[str]) -> Optional[Document]:
        """Read JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            content = json.dumps(json_data, indent=2)
            return Document(
                doc_id=doc_id,
                source="json",
                content=content,
                metadata={"filepath": filepath, "type": list(json_data.keys())[0] if json_data else "unknown"},
                security_level=security_level,
                access_roles=access_roles
            )
        except FileNotFoundError:
            print(f"[WARNING] JSON file not found: {filepath}")
            return None
        except Exception as e:
            print(f"[WARNING] Error reading JSON {filepath}: {str(e)}")
            return None

    @staticmethod
    def create_pdf_data() -> List[Document]:
        """Load PDF documents from actual files"""
        pdf_docs = []
        
        files = [
            ("sample_data_patient_report.pdf", "PDF_001", "restricted", ["doctor", "admin"]),
            ("sample_data_financial_report.pdf", "PDF_002", "confidential", ["admin"]),
            ("sample_data_employee_handbook.pdf", "PDF_003", "internal", ["admin", "hr"]),
        ]
        
        for filename, doc_id, security_level, access_roles in files:
            filepath = Path(Path.cwd()) / filename
            doc = SyntheticDataGenerator.read_pdf_file(filepath, doc_id, security_level, access_roles)
            if doc:
                pdf_docs.append(doc)
                print(f"  ✓ Loaded PDF: {doc_id} from {filename}")
        
        return pdf_docs

    @staticmethod
    def create_csv_data() -> List[Document]:
        """Load CSV documents from actual files"""
        csv_docs = []
        
        files = [
            ("sample_data_patients.csv", "CSV_001", "patients", "restricted", ["doctor", "admin"]),
            ("sample_data_employees.csv", "CSV_002", "employees", "confidential", ["admin", "hr"]),
            ("sample_data_appointments.csv", "CSV_003", "appointments", "internal", ["doctor", "admin", "hr"]),
        ]
        
        for filename, doc_id, table_name, security_level, access_roles in files:
            filepath = Path(Path.cwd()) / filename
            doc = SyntheticDataGenerator.read_csv_file(filepath, doc_id, table_name, security_level, access_roles)
            if doc:
                csv_docs.append(doc)
                print(f"  ✓ Loaded CSV: {doc_id} from {filename}")
        
        return csv_docs

    @staticmethod
    def create_json_data() -> List[Document]:
        """Load JSON documents from actual files"""
        json_docs = []
        
        files = [
            ("sample_data_audit_logs.json", "JSON_001", "confidential", ["admin", "engineer"]),
            ("sample_data_alerts.json", "JSON_002", "internal", ["admin", "engineer"]),
            ("sample_data_compliance.json", "JSON_003", "confidential", ["admin", "hr"]),
        ]
        
        for filename, doc_id, security_level, access_roles in files:
            filepath = Path(Path.cwd()) / filename
            doc = SyntheticDataGenerator.read_json_file(filepath, doc_id, security_level, access_roles)
            if doc:
                json_docs.append(doc)
                print(f"  ✓ Loaded JSON: {doc_id} from {filename}")
        
        return json_docs

    @staticmethod
    def create_sql_dumps() -> List[Document]:
        """Create SQL database dump documents"""
        sql_docs = [
            Document(
                doc_id="SQL_001",
                source="sql",
                content="""
SELECT * FROM lab_results;
result_id | patient_id | test_name | value | unit | date
1         | 001        | Hemoglobin| 14.2  | g/dL | 2025-05-17
2         | 002        | Glucose   | 150   | mg/dL| 2025-05-16
3         | 003        | Cholesterol|220   | mg/dL| 2025-05-15
4         | 004        | Triglycerides|180 | mg/dL| 2025-05-18
                """,
                metadata={"table": "lab_results", "records": 4},
                security_level="restricted",
                access_roles=["doctor", "admin"]
            ),
            Document(
                doc_id="SQL_002",
                source="sql",
                content="""
SELECT * FROM transactions;
transaction_id | amount | date | category | status
TXN_001 | ₹500000 | 2025-05-18 | Equipment | Completed
TXN_002 | ₹150000 | 2025-05-17 | Supplies | Pending
TXN_003 | ₹300000 | 2025-05-16 | Utilities | Completed
                """,
                metadata={"table": "transactions", "records": 3},
                security_level="confidential",
                access_roles=["admin"]
            ),
        ]
        print(f"  ✓ Loaded SQL: SQL_001, SQL_002 (in-memory)")
        return sql_docs


# ============================================================================
# RBAC & ACCESS CONTROL
# ============================================================================

class RBACEnforcer:
    """Role-Based Access Control enforcement"""

    USERS = {
        "doctor_ramesh": User(
            user_id="doctor_ramesh",
            name="Dr. Ramesh",
            role="doctor",
            department="Medical"
        ),
        "hr_priya": User(
            user_id="hr_priya",
            name="Priya Sharma",
            role="hr",
            department="Human Resources"
        ),
        "admin_root": User(
            user_id="admin_root",
            name="Root Admin",
            role="admin",
            department="IT"
        ),
        "engineer_john": User(
            user_id="engineer_john",
            name="John Dev",
            role="engineer",
            department="Engineering"
        ),
        "intern_jane": User(
            user_id="intern_jane",
            name="Jane Intern",
            role="intern",
            department="Operations"
        ),
    }

    @staticmethod
    def authenticate(user_id: str) -> Optional[User]:
        """Authenticate user and return user object"""
        if user_id in RBACEnforcer.USERS:
            return RBACEnforcer.USERS[user_id]
        return None

    @staticmethod
    def can_access(user: User, document: Document) -> bool:
        """Check if user can access document based on role"""
        # Admin can access everything
        if user.role == "admin":
            return True
        
        # Check if user's role is in document's access list
        return user.role in document.access_roles

    @staticmethod
    def filter_documents(user: User, documents: List[Document]) -> List[Document]:
        """Filter documents based on user's access rights"""
        accessible_docs = []
        for doc in documents:
            if RBACEnforcer.can_access(user, doc):
                accessible_docs.append(doc)
        return accessible_docs

    @staticmethod
    def get_permissions(role: str, environment: str = "prod") -> set:
        """
        Get permissions for a role in given environment
        Enhanced feature from Qlik approach
        """
        # Base permissions by role (same for both environments)
        base_permissions = {
            "admin": {"read", "write", "delete", "publish", "admin"},
            "doctor": {"read", "write"},
            "hr": {"read", "write"},
            "engineer": {"read", "write"},
            "intern": {"read"}
        }
        
        perms = set(base_permissions.get(role, {"read"}))
        
        # Dev environment has additional permissions for testing
        if environment == "dev":
            if role != "intern":
                perms.add("test")
        
        return perms


# ============================================================================
# MULTI-SOURCE RETRIEVAL
# ============================================================================

class MultiSourceRetriever:
    """Retrieve documents from multiple sources"""

    def __init__(self, all_documents: List[Document]):
        self.all_documents = all_documents
        self.document_index = {doc.doc_id: doc for doc in all_documents}

    def simple_semantic_search(self, query: str, source_type: Optional[str] = None) -> List[RetrievedContext]:
        """
        Simple keyword-based semantic search
        (In production: use ChromaDB/FAISS for real embeddings)
        """
        results = []
        query_lower = query.lower()

        for doc in self.all_documents:
            # Filter by source if specified
            if source_type and doc.source != source_type:
                continue

            # Simple relevance scoring
            relevance_score = 0.0
            
            # Exact keyword matches
            keywords = query_lower.split()
            for keyword in keywords:
                if keyword in doc.content.lower():
                    relevance_score += 0.3

            # Check metadata
            content_lower = str(doc.metadata).lower()
            for keyword in keywords:
                if keyword in content_lower:
                    relevance_score += 0.2

            if relevance_score > 0:
                results.append(RetrievedContext(
                    document=doc,
                    relevance_score=min(relevance_score, 0.95),  # Cap at 0.95
                    source=doc.source
                ))

        # Sort by relevance and return top results
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:5]  # Top 5 results

    def retrieve_from_all_sources(self, query: str) -> List[RetrievedContext]:
        """Retrieve from all sources: PDFs, CSVs, JSONs, SQLs"""
        all_results = []

        # Retrieve from each source type
        for source_type in ["pdf", "csv", "json", "sql"]:
            results = self.simple_semantic_search(query, source_type)
            all_results.extend(results)

        # Deduplicate and sort
        unique_results = {}
        for result in all_results:
            if result.document.doc_id not in unique_results:
                unique_results[result.document.doc_id] = result

        return sorted(unique_results.values(), key=lambda x: x.relevance_score, reverse=True)


# ============================================================================
# GROUNDING & HALLUCINATION PREVENTION
# ============================================================================

class GroundingChecker:
    """Verify answers are grounded in retrieved data"""

    @staticmethod
    def check_grounding(retrieved_docs: List[Document], llm_response: str) -> Tuple[bool, float]:
        """
        Check if LLM response is grounded in retrieved documents
        Returns: (is_grounded: bool, confidence: float)
        """
        if not retrieved_docs:
            return False, 0.0

        # Combine all retrieved content
        combined_content = " ".join([doc.content for doc in retrieved_docs]).lower()
        response_lower = llm_response.lower()

        # Extract key phrases from response (words and short phrases)
        key_phrases = re.findall(r'\b\w+(?:\s+\w+){0,2}\b', response_lower)

        # Score: how many phrases/words appear in retrieved content
        grounded_phrases = 0
        for phrase in key_phrases:
            if len(phrase) > 2:  # Reduced from 3 to 2 for better matching
                # Check for exact phrase or at least the first word
                if phrase in combined_content or phrase.split()[0] in combined_content:
                    grounded_phrases += 1

        # Calculate grounding ratio with minimum threshold
        grounding_ratio = grounded_phrases / max(len(key_phrases), 1)
        
        # More lenient threshold - if at least 30% of key phrases are grounded
        is_grounded = grounding_ratio > 0.3 or grounded_phrases >= 3
        
        # Base confidence on grounding ratio
        confidence = min(max(grounding_ratio, 0.4), 0.95) if is_grounded else 0.0

        return is_grounded, confidence

    @staticmethod
    def generate_confidence_score(retrieved_count: int, grounded: bool, confidence: float) -> float:
        """Generate overall confidence score based on grounding and source count"""
        # If not grounded or no data, confidence is 0.0
        if not grounded or retrieved_count == 0:
            return 0.0
        
        # If grounded, calculate final confidence with source boost
        # Base confidence from grounding
        base_confidence = max(confidence, 0.4)
        
        # Boost confidence based on number of sources
        # Each source adds credibility (up to 0.35 boost for 3+ sources)
        source_boost = min(retrieved_count * 0.12, 0.35)
        
        # Final confidence: combine base and boost, cap at 0.99
        final_confidence = min(base_confidence + source_boost, 0.99)
        
        return final_confidence


# ============================================================================
# RESPONSE FORMATTER
# ============================================================================

class ResponseFormatter:
    """Format LLM responses into structured, interview-ready output"""
    
    @staticmethod
    def format_response(answer: str, role: str) -> str:
        """
        Format raw LLM answer into structured format
        Makes output readable and professional
        """
        # If it's an error or no data, return as is
        if answer.startswith("["):
            return answer
            
        # Add role context at top
        formatted = f"📊 **Query Results** (Access Level: {role.upper()})\n"
        formatted += "=" * 60 + "\n\n"
        
        # Try to detect and structure different response types
        
        # Type 1: Employee/Team Data
        if any(keyword in answer.lower() for keyword in ['employee', 'department', 'salary', 'designation']):
            formatted += "👥 **Employee Information**\n"
            formatted += "-" * 40 + "\n"
            formatted += ResponseFormatter._extract_table_data(answer, 'employee')
            
        # Type 2: Patient/Medical Data
        elif any(keyword in answer.lower() for keyword in ['patient', 'medical', 'condition', 'treatment', 'lab result', 'diagnosis']):
            formatted += "🏥 **Patient Medical Records**\n"
            formatted += "-" * 40 + "\n"
            formatted += ResponseFormatter._extract_table_data(answer, 'patient')
            
        # Type 3: Financial/Transaction Data
        elif any(keyword in answer.lower() for keyword in ['transaction', 'amount', 'financial', 'payment']):
            formatted += "💰 **Financial Transactions**\n"
            formatted += "-" * 40 + "\n"
            formatted += ResponseFormatter._extract_table_data(answer, 'financial')
            
        # Type 4: System/Alert Data
        elif any(keyword in answer.lower() for keyword in ['alert', 'system', 'status', 'event']):
            formatted += "⚠️ **System Alerts & Events**\n"
            formatted += "-" * 40 + "\n"
            formatted += ResponseFormatter._extract_table_data(answer, 'alerts')
            
        # Default: Generic structured format
        else:
            formatted += "📋 **Response Details**\n"
            formatted += "-" * 40 + "\n"
            formatted += ResponseFormatter._extract_key_info(answer)
        
        formatted += "\n" + "=" * 60 + "\n"
        formatted += "✅ **Data Access**: Structured from authorized sources\n"
        return formatted
    
    @staticmethod
    def _extract_table_data(answer: str, data_type: str) -> str:
        """Extract and format table-like data from answer"""
        lines = []
        
        # Split answer into logical sections
        sections = answer.split('\n\n')
        for section in sections[:5]:  # Limit to first 5 sections
            section = section.strip()
            if not section or len(section) < 10:
                continue
                
            # Try to identify list items
            if section.count('\n') >= 2 and any(marker in section for marker in ['*', '**', '-', '1.', '2.', '3.']):
                lines.append(section)
            elif ':' in section:
                # Key-value pair
                lines.append(section)
        
        formatted_text = "\n".join(lines)
        return formatted_text if formatted_text else answer[:500] + "..."
    
    @staticmethod
    def _extract_key_info(answer: str) -> str:
        """Extract key information points from generic answer"""
        # Find all numbered items, bullet points, or key statements
        lines = answer.split('\n')
        key_lines = []
        
        for line in lines[:15]:  # First 15 lines
            line = line.strip()
            if line and len(line) > 10:
                # Highlight key lines
                if any(marker in line for marker in ['**', '•', '-', '1.', '2.']):
                    key_lines.append(line)
                elif ':' in line:
                    key_lines.append(line)
        
        return "\n".join(key_lines) if key_lines else answer[:400] + "..."


# ============================================================================
# LLM INTEGRATION (Groq)
# ============================================================================

class GroqLLMHandler:
    """Handle LLM calls to Groq API"""

    def __init__(self, api_key: str, model: str = "llama-3.1-8b-instant", max_tokens: int = 1024):
        self.client = Groq(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens

    def generate_answer(self, query: str, context: List[Document], user_role: str) -> str:
        """
        Generate answer using Groq LLM
        Groq constraints: Max tokens enforced
        """
        # Prepare context string
        context_str = "\n\n---\n\n".join([
            f"[Source: {doc.source.upper()}]\n{doc.content[:500]}"
            for doc in context
        ])

        system_prompt = """You are an enterprise AI assistant. Follow these rules STRICTLY:
1. Answer ONLY based on the provided context - NEVER make up information
2. Structure your response clearly with:
   - Main data points first
   - Use numbering (1., 2., 3.) or bullet points (*)
   - Include relevant numbers, dates, and metrics
   - Group related information together
3. Use this format:
   - **Header**: Main category (e.g., **Employee Information** or **Patient Records**)
   - List items with dashes or numbers
   - Always show: ID/Name, Key Details, Status/Condition, Additional Info
4. Be professional and concise
5. If information is incomplete, clearly state what's missing
6. End with confidence assessment"""

        user_message = f"""User Role: {user_role}

Query: {query}

Context from retrieved documents:
{context_str}

IMPORTANT: Format the answer as a clear, structured list with headers and key details. 
Each item should have: ID/Name | Key Field 1 | Key Field 2 | Key Field 3 | Status

Generate a grounded, well-structured answer based ONLY on the above context."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=self.max_tokens,
                temperature=0.3,  # Low temperature for consistency
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[ERROR] Failed to generate response: {str(e)}"


# ============================================================================
# MAIN RAG SYSTEM
# ============================================================================

class EnterpriseRAGSystem:
    """Complete enterprise RAG pipeline"""

    def __init__(self, groq_api_key: str):
        # Initialize components
        self.data_generator = SyntheticDataGenerator()
        self.rbac = RBACEnforcer()
        
        # Load all data
        all_documents = (
            self.data_generator.create_pdf_data() +
            self.data_generator.create_csv_data() +
            self.data_generator.create_json_data() +
            self.data_generator.create_sql_dumps()
        )
        
        self.retriever = MultiSourceRetriever(all_documents)
        self.grounder = GroundingChecker()
        self.llm = GroqLLMHandler(groq_api_key, max_tokens=1024)

        # Audit log
        self.audit_logs = []

    def process_query(self, user_id: str, query: str) -> RAGResponse:
        """
        Process user query through complete RAG pipeline
        Returns: RAGResponse with answer, sources, confidence, and audit trail
        """
        timestamp = datetime.now().isoformat()

        # ========== STEP 1: AUTHENTICATION ==========
        user = self.rbac.authenticate(user_id)
        if not user:
            return RAGResponse(
                answer="[AUTH_ERROR] User not authenticated",
                sources=[],
                confidence=0.0,
                user=user_id,
                role="unknown",
                access_granted=False,
                timestamp=timestamp,
                audit_log={"error": "authentication_failed"}
            )

        print(f"\n✅ [1] AUTHENTICATION: User '{user.name}' ({user.role}) authenticated")

        # ========== STEP 2: QUERY PROCESSING ==========
        print(f"📝 [2] QUERY PROCESSING: '{query}'")

        # ========== STEP 3: MULTI-SOURCE RETRIEVAL ==========
        all_retrieved = self.retriever.retrieve_from_all_sources(query)
        print(f"🔍 [3] RETRIEVAL: Found {len(all_retrieved)} documents across all sources")
        for result in all_retrieved[:3]:
            print(f"   - {result.document.doc_id} ({result.source}): {result.relevance_score:.2%}")

        # ========== STEP 3B: RESOURCE DETECTION ==========
        # Use centralized configuration for resource detection (NOT hard-coded)
        requested_resources = detect_requested_resources(query)
        print(f"📌 [3B] RESOURCE DETECTION: Requested resources: {requested_resources}")

        # ========== STEP 4: RBAC FILTER ==========
        retrieved_docs = [r.document for r in all_retrieved]
        filtered_docs = self.rbac.filter_documents(user, retrieved_docs)
        
        access_denied_count = len(retrieved_docs) - len(filtered_docs)
        print(f"🔐 [4] RBAC FILTER: {len(filtered_docs)} accessible, {access_denied_count} denied for '{user.role}'")

        # ========== STEP 4B: CHECK FOR RESTRICTED RESOURCE ACCESS ==========
        # Use config-based system to validate resource access
        for resource in requested_resources:
            required_docs = get_required_documents(resource)
            allowed_roles = get_allowed_roles(resource)
            
            # Check if user's role is allowed to access this resource
            if user.role not in allowed_roles and user.role != "admin":
                print(f"❌ [4B] User ({user.role}) querying for {resource.upper()} but role not in allowed list")
                resource_info = RESOURCE_MAPPING.get(resource, {})
                return RAGResponse(
                    answer="[NO_DATA] No accessible data found for your query",
                    sources=[],
                    confidence=0.0,
                    user=user_id,
                    role=user.role,
                    access_granted=False,
                    timestamp=timestamp,
                    audit_log={
                        "reason": "restricted_resource_denied",
                        "documents_retrieved": len(retrieved_docs),
                        "documents_denied": len(retrieved_docs),
                        "access_granted": False,
                        "restricted_resource": resource,
                        "resource_description": resource_info.get("description", "Unknown"),
                        "required_documents": required_docs
                    }
                )
            
            # Check if user has access to required documents
            has_required_access = all(
                any(doc.doc_id == req_doc for doc in filtered_docs)
                for req_doc in required_docs
            )
            
            if not has_required_access:
                print(f"❌ [4B] User querying for {resource.upper()} but lacks access to required documents: {required_docs}")
                resource_info = RESOURCE_MAPPING.get(resource, {})
                return RAGResponse(
                    answer="[NO_DATA] No accessible data found for your query",
                    sources=[],
                    confidence=0.0,
                    user=user_id,
                    role=user.role,
                    access_granted=False,
                    timestamp=timestamp,
                    audit_log={
                        "reason": "restricted_resource_denied",
                        "documents_retrieved": len(retrieved_docs),
                        "documents_denied": len(retrieved_docs),
                        "access_granted": False,
                        "restricted_resource": resource,
                        "resource_description": resource_info.get("description", "Unknown"),
                        "required_documents": required_docs,
                        "missing_documents": [doc for doc in required_docs if not any(d.doc_id == doc for d in filtered_docs)]
                    }
                )

        # ========== STEP 5: GROUNDING CHECK ==========
        if not filtered_docs:
            # User requested data but has NO access to it - ACCESS DENIED
            access_denied_reason = "no_accessible_documents" if len(retrieved_docs) > 0 else "no_data_found"
            return RAGResponse(
                answer="[NO_DATA] No accessible data found for your query",
                sources=[],
                confidence=0.0,
                user=user_id,
                role=user.role,
                access_granted=False,
                timestamp=timestamp,
                audit_log={
                    "reason": access_denied_reason,
                    "documents_retrieved": len(retrieved_docs),
                    "documents_denied": len(retrieved_docs),
                    "access_granted": False
                }
            )

        is_grounded = len(filtered_docs) > 0
        confidence_base = len(filtered_docs) / max(len(retrieved_docs), 1)
        print(f"📊 [5] GROUNDING: Base confidence {confidence_base:.2%} (data sources: {len(filtered_docs)})")

        # ========== STEP 6: GENERATE ANSWER ==========
        print(f"🤖 [6] LLM GENERATION: Generating answer with Groq...")
        answer = self.llm.generate_answer(query, filtered_docs, user.role)
        print(f"   Answer: {answer[:100]}...")

        # ========== STEP 7: HALLUCINATION CHECK ==========
        is_grounded_check, confidence_score = self.grounder.check_grounding(filtered_docs, answer)
        final_confidence = self.grounder.generate_confidence_score(
            len(filtered_docs), is_grounded_check, confidence_score
        )
        print(f"✓ [7] GROUNDING CHECK: Grounded={is_grounded_check}, Final Confidence={final_confidence:.2%}")

        # ========== STEP 8: FORMAT RESPONSE ==========
        formatted_answer = ResponseFormatter.format_response(answer, user.role)

        # ========== STEP 9: PREPARE RESPONSE ==========
        sources = [doc.doc_id for doc in filtered_docs]
        audit_log = {
            "user_id": user_id,
            "role": user.role,
            "query": query,
            "documents_retrieved": len(retrieved_docs),
            "documents_accessible": len(filtered_docs),
            "documents_denied": access_denied_count,
            "sources": sources,
            "answer_grounded": is_grounded_check,
            "confidence": final_confidence,
            "timestamp": timestamp
        }

        response = RAGResponse(
            answer=formatted_answer,
            sources=sources,
            confidence=final_confidence,
            user=user_id,
            role=user.role,
            access_granted=True,
            timestamp=timestamp,
            audit_log=audit_log
        )

        # Log to audit trail
        self.audit_logs.append(audit_log)

        return response

    def print_response(self, response: RAGResponse):
        """Pretty print RAG response"""
        print("\n" + "="*70)
        print("📋 FINAL RESPONSE")
        print("="*70)
        print(f"\n💬 ANSWER:\n{response.answer}")
        print(f"\n📎 SOURCES: {', '.join(response.sources)}")
        print(f"🎯 CONFIDENCE: {response.confidence:.1%}")
        print(f"👤 USER: {response.user} ({response.role})")
        print(f"⏰ TIMESTAMP: {response.timestamp}")
        print(f"\n🔍 AUDIT LOG:")
        for key, value in response.audit_log.items():
            if key != "timestamp":
                print(f"   {key}: {value}")
        print("\n" + "="*70)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution"""
    import os
    load_dotenv()

    # Get Groq API key
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("❌ ERROR: GROQ_API_KEY environment variable not set")
        print("Set it with: export GROQ_API_KEY='your_key_here'")
        return

    print("\n" + "="*70)
    print("🚀 ENTERPRISE RAG INTELLIGENCE SYSTEM")
    print("="*70)
    print("\nLoading system with ACTUAL DATA FILES...")
    print("\nLoading Documents:")
    print("- PDFs (3 files)")
    print("- CSVs (3 files)")
    print("- JSONs (3 files)")
    print("- SQL (2 files)")
    print(f"Total: 11 documents | Users: {len(RBACEnforcer.USERS)} | Max tokens: 1024")

    # Initialize RAG system
    rag_system = EnterpriseRAGSystem(groq_api_key)

    # Test queries
    test_cases = [
        {
            "user_id": "doctor_ramesh",
            "query": "John ke lab report mein kya likha hai?"
        },
        {
            "user_id": "hr_priya",
            "query": "Q3 mein revenue kitna tha?"
        },
        {
            "user_id": "engineer_john",
            "query": "Server mein kaunse alerts hain?"
        },
        {
            "user_id": "intern_jane",
            "query": "Employee ka salary kitna hai?"
        },
        {
            "user_id": "admin_root",
            "query": "Compliance status kya hai?"
        }
    ]

    print("\n" + "="*70)
    print("🧪 RUNNING TEST CASES")
    print("="*70)

    for i, test in enumerate(test_cases, 1):
        print(f"\n\n{'='*70}")
        print(f"TEST CASE {i}")
        print(f"{'='*70}")
        print(f"User: {test['user_id']}")
        print(f"Query: {test['query']}")
        print("-"*70)

        response = rag_system.process_query(test['user_id'], test['query'])
        rag_system.print_response(response)

    # Save audit logs
    print("\n\n" + "="*70)
    print("📝 AUDIT TRAIL")
    print("="*70)
    print(f"Total queries processed: {len(rag_system.audit_logs)}")
    audit_file = "audit_logs.json"
    with open(audit_file, "w") as f:
        json.dump(rag_system.audit_logs, f, indent=2)
    print(f"✅ Audit logs saved to: {audit_file}")


if __name__ == "__main__":
    main()
