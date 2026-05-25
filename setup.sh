#!/bin/bash

# Enterprise RAG System - Setup Script
# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🚀 Enterprise RAG System Setup${NC}"
echo -e "${BLUE}========================================${NC}"

# Check Python version
echo -e "\n${YELLOW}[1] Checking Python version...${NC}"
python3 --version
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Python3 not found. Please install Python 3.8+${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python3 found${NC}"

# Create virtual environment
echo -e "\n${YELLOW}[2] Creating virtual environment...${NC}"
python3 -m venv rag_env
source rag_env/bin/activate
echo -e "${GREEN}✅ Virtual environment created${NC}"

# Upgrade pip
echo -e "\n${YELLOW}[3] Upgrading pip...${NC}"
pip install --upgrade pip -q
echo -e "${GREEN}✅ pip upgraded${NC}"

# Install required packages
echo -e "\n${YELLOW}[4] Installing dependencies...${NC}"
pip install -q \
    groq>=0.4.1 \
    python-dotenv>=1.0.0 \
    PyPDF2>=3.0.0 \
    pandas>=2.0.0

echo -e "${GREEN}✅ Dependencies installed${NC}"

# Check for Groq API key
echo -e "\n${YELLOW}[5] Checking Groq API key...${NC}"
if [ -z "$GROQ_API_KEY" ]; then
    echo -e "${RED}⚠️  GROQ_API_KEY environment variable not set${NC}"
    echo -e "${YELLOW}Set it with:${NC}"
    echo -e "${BLUE}export GROQ_API_KEY='your_api_key_here'${NC}"
    echo -e "\n${YELLOW}Get API key from: https://console.groq.com/keys${NC}"
else
    echo -e "${GREEN}✅ GROQ_API_KEY is set${NC}"
fi

# Display next steps
echo -e "\n${BLUE}========================================${NC}"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "\n${YELLOW}Next steps:${NC}"
echo -e "1. Set Groq API key (if not already set):"
echo -e "   ${BLUE}export GROQ_API_KEY='your_api_key_here'${NC}"
echo -e "\n2. Activate virtual environment:"
echo -e "   ${BLUE}source rag_env/bin/activate${NC}"
echo -e "\n3. Run the system:"
echo -e "   ${BLUE}python3 enterprise_rag_system.py${NC}"
echo -e "\n${BLUE}========================================${NC}"
