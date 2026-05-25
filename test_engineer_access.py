#!/usr/bin/env python3
"""Quick test for Engineer access control"""
import requests

tests = [
    ('engineer_john', 'What patient records are there?', 'Engineer - Patient Data (DENY)'),
    ('engineer_john', 'Show me audit logs and system events', 'Engineer - Audit Logs (ALLOW)'),
    ('engineer_john', 'What employee data exists?', 'Engineer - Employee Data (DENY)'),
    ('doctor_ramesh', 'What are patient medical conditions?', 'Doctor - Patient Data (ALLOW)'),
    ('hr_priya', 'List employees with salaries', 'HR - Employee Data (ALLOW)'),
]

print("\n" + "="*80)
print("COMPREHENSIVE RESOURCE ACCESS CONTROL TEST")
print("="*80 + "\n")

for user, query, label in tests:
    try:
        response = requests.post(
            'http://localhost:8000/api/query',
            json={'user_id': user, 'query': query, 'environment': 'prod'},
            timeout=10
        )
        data = response.json()
        access = data.get('access_granted')
        conf = data.get('confidence')
        ans = data.get('answer')[:70]
        sources = len(data.get('sources', []))
        
        status = "✅ PASS" if access else "❌ DENY"
        
        print(f"{status} | {label}")
        print(f"    Access: {access} | Confidence: {conf:.1%} | Sources: {sources}")
        print(f"    Answer: {ans}...")
        print()
    except Exception as e:
        print(f"❌ ERROR | {label}: {str(e)}\n")

print("="*80)
