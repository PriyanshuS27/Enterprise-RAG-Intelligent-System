#!/usr/bin/env python3
"""
Complete Test Suite for Sample Questions
Tests all sample questions from HTML for each user role
"""

import requests
import json
import time
import subprocess
import sys
import os
from datetime import datetime

# API Base URL
BASE_URL = "http://localhost:8000"

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Sample questions from HTML
SAMPLE_QUESTIONS = {
    "doctor_ramesh": [
        "List all patients with their medical conditions",
        "What is John Doe's condition and admission date?",
        "Who has Hypertension? Show patient details"
    ],
    "hr_priya": [
        "List all employees with their departments",
        "What is Amit Kumar's salary and designation?",
        "Show all employees in Engineering department"
    ],
    "admin_root": [
        "Show all user access audit logs",
        "What actions did doctor_ramesh perform?",
        "Show all successful access records"
    ],
    "engineer_john": [
        "What are the current system alerts?",
        "Show me high severity alerts with their details",
        "What database connection issues exist?"
    ],
    "intern_jane": [
        "What is the company environment status?",
        "Show me system infrastructure information",
        "What compliance data is available?"
    ]
}

def print_header(text):
    """Print formatted header"""
    print(f"\n{BOLD}{BLUE}{'='*100}{RESET}")
    print(f"{BOLD}{BLUE}{text:^100}{RESET}")
    print(f"{BOLD}{BLUE}{'='*100}{RESET}\n")

def print_section(text):
    """Print formatted section"""
    print(f"\n{BOLD}{CYAN}>>> {text}{RESET}")

def print_success(text):
    """Print success message"""
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    """Print error message"""
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    """Print warning message"""
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    """Print info message"""
    print(f"{BLUE}ℹ️  {text}{RESET}")

def test_api_health():
    """Check if API is running"""
    print_section("Checking API Health")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print_success("API is running and healthy")
            return True
        else:
            print_error(f"API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to API. Is the Flask server running?")
        return False
    except Exception as e:
        print_error(f"Error checking API health: {str(e)}")
        return False

def test_question(user_id, question_num, question):
    """Test a single question"""
    print_section(f"Question {question_num}: {question}")
    print(f"{BOLD}User:{RESET} {user_id}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/query",
            json={
                "user_id": user_id,
                "query": question
            },
            timeout=30
        )
        
        if response.status_code != 200:
            print_error(f"API returned status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        data = response.json()
        
        # Check response structure
        if data.get("status") != "success":
            print_error(f"Query failed: {data.get('answer', 'Unknown error')}")
            return False
        
        # Extract key information
        answer = data.get("answer", "")
        confidence = data.get("confidence", 0)
        sources = data.get("sources", [])
        accessible = data.get("accessible", 0)
        denied = data.get("denied", 0)
        
        # Print results
        print(f"{BOLD}Answer:{RESET}")
        print(f"  {answer[:200]}..." if len(answer) > 200 else f"  {answer}")
        
        # Confidence score
        confidence_pct = confidence * 100
        if confidence >= 0.85:
            confidence_color = GREEN
        elif confidence >= 0.70:
            confidence_color = YELLOW
        else:
            confidence_color = RED
        
        print(f"{BOLD}Confidence:{RESET} {confidence_color}{confidence_pct:.1f}%{RESET}")
        print(f"{BOLD}Sources:{RESET} {len(sources)} sources retrieved")
        for source in sources:
            print(f"  • {source}")
        
        print(f"{BOLD}Access Control:{RESET}")
        print(f"  • Accessible: {GREEN}{accessible}{RESET}")
        print(f"  • Denied: {RED}{denied}{RESET}")
        
        # Determine pass/fail based on confidence
        if confidence >= 0.70:
            print_success(f"Question answered with {confidence_pct:.1f}% confidence")
            return True
        else:
            print_warning(f"Low confidence ({confidence_pct:.1f}%)")
            return False
            
    except requests.exceptions.Timeout:
        print_error("Request timeout (30s exceeded)")
        return False
    except Exception as e:
        print_error(f"Error testing question: {str(e)}")
        return False

def test_all_sample_questions():
    """Test all sample questions for all users"""
    print_header("ENTERPRISE RAG SAMPLE QUESTIONS TEST")
    print_info(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check API health
    if not test_api_health():
        print_error("\n❌ API is not running! Starting Flask API...")
        print_info("Please ensure Flask API is running on http://localhost:8000")
        return False
    
    # Test results tracker
    results = {}
    total_tests = 0
    passed_tests = 0
    
    # Test each user
    for user_id, questions in SAMPLE_QUESTIONS.items():
        user_name = {
            "doctor_ramesh": "👨‍⚕️ Dr. Ramesh (Doctor)",
            "hr_priya": "👩‍💼 Priya Sharma (HR)",
            "admin_root": "🔐 Root Admin (Admin)",
            "engineer_john": "👨‍💻 John Dev (Engineer)",
            "intern_jane": "👨‍🎓 Jane Intern (Intern)"
        }.get(user_id, user_id)
        
        print_header(f"USER: {user_name}")
        results[user_id] = {"name": user_name, "passed": 0, "total": 0, "questions": []}
        
        # Test each question for this user
        for q_num, question in enumerate(questions, 1):
            total_tests += 1
            results[user_id]["total"] += 1
            
            success = test_question(user_id, q_num, question)
            results[user_id]["questions"].append({
                "question": question,
                "passed": success
            })
            
            if success:
                passed_tests += 1
                results[user_id]["passed"] += 1
            
            time.sleep(1)  # Rate limiting
    
    # Print summary
    print_header("TEST SUMMARY")
    
    print(f"{BOLD}Overall Results:{RESET}")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {GREEN}{passed_tests}{RESET}")
    print(f"  Failed: {RED}{total_tests - passed_tests}{RESET}")
    print(f"  Success Rate: {GREEN}{(passed_tests/total_tests*100):.1f}%{RESET}")
    
    print(f"\n{BOLD}Results by User:{RESET}")
    for user_id, user_results in results.items():
        passed = user_results["passed"]
        total = user_results["total"]
        pct = (passed/total*100) if total > 0 else 0
        
        color = GREEN if pct >= 70 else YELLOW if pct >= 50 else RED
        print(f"\n{user_results['name']}")
        print(f"  Passed: {color}{passed}/{total} ({pct:.1f}%){RESET}")
        
        for q in user_results["questions"]:
            status = "✅" if q["passed"] else "❌"
            print(f"    {status} {q['question'][:70]}")
    
    print_info(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return passed_tests / total_tests >= 0.70

if __name__ == "__main__":
    success = test_all_sample_questions()
    sys.exit(0 if success else 1)
