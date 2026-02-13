# SPDX-License-Identifier: Apache-2.0
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

#!/bin/bash
# Setup script for local development with LangChain examples

set -e

echo "🚀 Setting up LangChain examples for local development..."
echo ""

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from examples/langchain directory"
    exit 1
fi

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the examples, you need to set environment variables:"
echo ""
echo "  export OPENAI_API_KEY='your-api-key-here'"
echo "  export DATAHUB_GMS_URL='http://localhost:8080'  # Optional, this is the default"
echo ""
echo "Then run any example:"
echo "  python simple_search.py"
echo "  python basic_agent.py"
echo ""
