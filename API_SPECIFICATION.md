# 🔌 Enterprise RAG System - API Specification

## Backend API Endpoints

### Base URL
```
http://localhost:8000/api
```

---

## Endpoints

### 1. Query RAG System
**Process a user query through the RAG pipeline**

```
POST /query
Content-Type: application/json

Request Body:
{
  "user_id": "doctor_ramesh",
  "query": "John ke lab report mein kya likha hai?"
}

Response (Success):
{
  "status": "success",
  "answer": "John ke lab report mein Hemoglobin ki value 14.2 g/dL aur WBC ki value 7000 hai...",
  "confidence": 0.637,
  "sources": ["PDF_001", "CSV_001", "SQL_001"],
  "user": "doctor_ramesh",
  "role": "doctor",
  "timestamp": "2026-05-19T01:35:20.903229",
  "documents_retrieved": 5,
  "documents_accessible": 3,
  "documents_denied": 2,
  "audit_log": {
    "user_id": "doctor_ramesh",
    "role": "doctor",
    "query": "John ke lab report mein kya likha hai?",
    "documents_retrieved": 5,
    "documents_accessible": 3,
    "documents_denied": 2,
    "sources": ["PDF_001", "CSV_001", "SQL_001"],
    "answer_grounded": true,
    "confidence": 0.637
  }
}

Response (Error - No Access):
{
  "status": "access_denied",
  "answer": "[NO_DATA] No accessible data found for your query",
  "confidence": 0.0,
  "reason": "no_accessible_documents"
}

Response (Error - Auth Failed):
{
  "status": "error",
  "error": "User not authenticated",
  "user_id": "invalid_user"
}
```

---

### 2. Get All Users
**Retrieve available users and their roles**

```
GET /users

Response:
{
  "status": "success",
  "users": [
    {
      "user_id": "doctor_ramesh",
      "name": "Dr. Ramesh",
      "role": "doctor",
      "department": "Medical",
      "avatar": "👨‍⚕️"
    },
    {
      "user_id": "hr_priya",
      "name": "Priya Sharma",
      "role": "hr",
      "department": "Human Resources",
      "avatar": "👩‍💼"
    },
    {
      "user_id": "admin_root",
      "name": "Root Admin",
      "role": "admin",
      "department": "IT",
      "avatar": "🔐"
    },
    {
      "user_id": "engineer_john",
      "name": "John Dev",
      "role": "engineer",
      "department": "Engineering",
      "avatar": "👨‍💻"
    },
    {
      "user_id": "intern_jane",
      "name": "Jane Intern",
      "role": "intern",
      "department": "Operations",
      "avatar": "👨‍🎓"
    }
  ],
  "total": 5
}
```

---

### 3. Get Documents
**Retrieve all indexed documents with metadata**

```
GET /documents

Response:
{
  "status": "success",
  "documents": [
    {
      "doc_id": "PDF_001",
      "source": "pdf",
      "filename": "sample_data_patient_report.pdf",
      "security_level": "restricted",
      "access_roles": ["doctor", "admin"],
      "content_length": 1523,
      "content_preview": "Patient Medical Report - John Doe..."
    },
    {
      "doc_id": "PDF_002",
      "source": "pdf",
      "filename": "sample_data_financial_report.pdf",
      "security_level": "confidential",
      "access_roles": ["admin", "finance"],
      "content_length": 892,
      "content_preview": "Q3 2025 Financial Report..."
    },
    ...
  ],
  "total": 11,
  "by_source": {
    "pdf": 3,
    "csv": 3,
    "json": 3,
    "sql": 2
  }
}
```

---

### 4. Get Audit Logs
**Retrieve access audit logs**

```
GET /audit-logs

Response:
{
  "status": "success",
  "logs": [
    {
      "user_id": "doctor_ramesh",
      "role": "doctor",
      "query": "John ke lab report mein kya likha hai?",
      "documents_retrieved": 5,
      "documents_accessible": 3,
      "documents_denied": 2,
      "sources": ["PDF_001", "CSV_001", "SQL_001"],
      "answer_grounded": true,
      "confidence": 0.637,
      "timestamp": "2026-05-19T01:35:20.903229"
    },
    {
      "user_id": "hr_priya",
      "role": "hr",
      "query": "Q3 mein revenue kitna tha?",
      "documents_retrieved": 1,
      "documents_accessible": 0,
      "documents_denied": 1,
      "reason": "no_accessible_documents",
      "timestamp": "2026-05-19T01:35:23.421716"
    },
    ...
  ],
  "total": 4
}
```

---

### 5. Get System Metrics
**Retrieve system performance metrics**

```
GET /metrics

Response:
{
  "status": "success",
  "metrics": {
    "total_queries": 4,
    "avg_response_time": 2.3,
    "avg_confidence": 0.637,
    "documents_indexed": 11,
    "users_count": 5,
    "uptime": "99.9%",
    "queries_by_role": {
      "doctor": 1,
      "hr": 1,
      "engineer": 1,
      "intern": 1,
      "admin": 0
    },
    "access_control": {
      "total_retrievals": 20,
      "granted": 15,
      "denied": 5,
      "grant_rate": "75%"
    },
    "document_stats": {
      "pdfs": 3,
      "csvs": 3,
      "jsons": 3,
      "sqls": 2
    }
  }
}
```

---

### 6. Get User Permissions
**Get what documents a user can access**

```
GET /users/:user_id/permissions

Response:
{
  "status": "success",
  "user_id": "doctor_ramesh",
  "role": "doctor",
  "permissions": {
    "accessible_documents": ["PDF_001", "CSV_001", "CSV_003", "SQL_001"],
    "denied_documents": ["PDF_002", "PDF_003", "CSV_002", "JSON_001", "JSON_002", "JSON_003", "SQL_002"],
    "total_accessible": 4,
    "total_denied": 7
  },
  "access_matrix": {
    "patient_records": true,
    "financial_data": false,
    "employee_data": false,
    "audit_logs": false,
    "compliance_data": false
  }
}
```

---

### 7. Get Query History
**Retrieve query history for a user**

```
GET /users/:user_id/history?limit=10

Response:
{
  "status": "success",
  "user_id": "doctor_ramesh",
  "queries": [
    {
      "query_id": "Q001",
      "query": "John ke lab report mein kya likha hai?",
      "answer": "John ke lab report mein...",
      "confidence": 0.637,
      "sources": ["PDF_001", "CSV_001"],
      "timestamp": "2026-05-19T01:35:20"
    }
  ],
  "total": 1
}
```

---

### 8. Test Connection
**Simple health check**

```
GET /health

Response:
{
  "status": "ok",
  "message": "Enterprise RAG System is running",
  "timestamp": "2026-05-19T01:35:20",
  "version": "1.0.0",
  "documents_loaded": 11
}
```

---

## Error Responses

### 400 - Bad Request
```json
{
  "status": "error",
  "error": "Invalid request format",
  "details": "Missing required field: user_id"
}
```

### 401 - Unauthorized
```json
{
  "status": "error",
  "error": "User not found",
  "user_id": "invalid_user"
}
```

### 403 - Forbidden
```json
{
  "status": "access_denied",
  "error": "Access denied",
  "reason": "No accessible documents for this query"
}
```

### 500 - Server Error
```json
{
  "status": "error",
  "error": "Internal server error",
  "details": "Failed to process query"
}
```

---

## Frontend Integration Example

### React Hook
```javascript
import { useState } from 'react';

export function useRAGQuery() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const query = async (userId, queryText) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          query: queryText
        })
      });
      
      if (!response.ok) throw new Error('Query failed');
      const data = await response.json();
      
      setIsLoading(false);
      return data;
    } catch (err) {
      setError(err.message);
      setIsLoading(false);
      throw err;
    }
  };

  return { query, isLoading, error };
}
```

### Usage in Component
```jsx
function QueryInterface() {
  const { query, isLoading } = useRAGQuery();
  const [results, setResults] = useState(null);

  const handleQuery = async (userId, queryText) => {
    const response = await query(userId, queryText);
    setResults(response);
  };

  return (
    <div>
      {isLoading && <Spinner />}
      {results && <ResultsDisplay results={results} />}
    </div>
  );
}
```

---

## CORS Configuration

### Python Backend (Flask)
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
  r"/api/*": {
    "origins": ["http://localhost:3000", "https://yourdomain.com"],
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type"]
  }
})
```

### Environment Variables
```env
# .env
GROQ_API_KEY=your_key_here
API_PORT=8000
CORS_ORIGIN=http://localhost:3000
```

---

## Rate Limiting (Future Enhancement)

```python
from flask_limiter import Limiter

limiter = Limiter(
  app=app,
  key_func=lambda: request.remote_addr,
  default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/query')
@limiter.limit("10 per minute")
def query_rag():
  ...
```

---

## Webhook Notifications (Future)

```python
@app.route('/webhooks/subscribe', methods=['POST'])
def subscribe_webhook():
  webhook_url = request.json['url']
  # Store webhook for event notifications
  
# Later, when query completes:
requests.post(webhook_url, json=results)
```

---

## API Versioning

```
v1: /api/v1/query
v2: /api/v2/query (future enhancements)
```

---

## Testing with cURL

```bash
# Query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "doctor_ramesh",
    "query": "John ke lab report?"
  }'

# Get Users
curl http://localhost:8000/api/users

# Get Metrics
curl http://localhost:8000/api/metrics

# Health Check
curl http://localhost:8000/api/health
```

---

## Response Time Optimization

| Endpoint | Avg Time | Max Time |
|----------|----------|----------|
| /query | 2-3s | 5s |
| /users | 10ms | 50ms |
| /documents | 20ms | 100ms |
| /audit-logs | 30ms | 150ms |
| /metrics | 50ms | 200ms |
| /health | <5ms | <10ms |

---

## Authentication (Future)

```python
@app.route('/api/auth/login', methods=['POST'])
def login():
  username = request.json['username']
  password = request.json['password']
  # Validate and return JWT token
  return jsonify({'token': jwt_token})

@app.route('/api/query', methods=['POST'])
@require_auth  # Decorator checks JWT
def query_rag():
  ...
```

---

**API Documentation Complete** ✅
