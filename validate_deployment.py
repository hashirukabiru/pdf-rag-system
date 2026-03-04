"""
Deployment Validation Script
Checks if all necessary files and dependencies are in place
"""

import sys
import os
from pathlib import Path

def check_file_exists(filepath, required=True):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else ("❌" if required else "⚠️")
    req_text = "REQUIRED" if required else "OPTIONAL"
    print(f"{status} {filepath} [{req_text}]")
    return exists

def check_import(module_name, required=True):
    """Check if a Python module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ {module_name} [INSTALLED]")
        return True
    except ImportError:
        status = "❌" if required else "⚠️"
        req_text = "REQUIRED" if required else "OPTIONAL"
        print(f"{status} {module_name} [MISSING - {req_text}]")
        return False

print("=" * 60)
print("🔍 DEPLOYMENT VALIDATION CHECK")
print("=" * 60)

# Check core Python files
print("\n📦 CORE APPLICATION FILES:")
core_files = [
    ("app.py", True),
    ("rag_system.py", True),
    ("pdf_processor.py", True),
    ("vector_store.py", True),
    ("llm_handler.py", True),
    ("config.py", True),
    ("cli.py", False),
]

all_core_exist = all(check_file_exists(f, req) for f, req in core_files)

# Check documentation
print("\n📚 DOCUMENTATION FILES:")
doc_files = [
    ("README.md", True),
    ("requirements.txt", True),
    ("LICENSE", True),
    (".gitignore", True),
    ("DEPLOYMENT_CHECKLIST.md", False),
    ("START_HERE.md", False),
]

all_docs_exist = all(check_file_exists(f, req) for f, req in doc_files)

# Check data directory
print("\n📁 DATA DIRECTORY:")
data_exists = check_file_exists("data", True)
if data_exists:
    pdf_files = list(Path("data").glob("*.pdf"))
    if pdf_files:
        print(f"  ✅ Found {len(pdf_files)} PDF file(s) for testing")
    else:
        print(f"  ⚠️  No PDF files found in data/ directory")

# Check Python dependencies
print("\n🐍 PYTHON DEPENDENCIES:")
required_deps = [
    "pypdf",
    "faiss",
    "numpy",
    "sentence_transformers",
    "gradio",
    "transformers",
    "torch",
]

optional_deps = [
    "ollama",
]

all_required = all(check_import(dep, True) for dep in required_deps)
for dep in optional_deps:
    check_import(dep, False)

# Check deployment files
print("\n🚀 DEPLOYMENT FILES:")
deployment_files = [
    ("Dockerfile", False),
    ("docker-compose.yml", False),
    (".env.example", False),
]

for f, req in deployment_files:
    check_file_exists(f, req)

# Final summary
print("\n" + "=" * 60)
print("📊 VALIDATION SUMMARY")
print("=" * 60)

issues = []
if not all_core_exist:
    issues.append("Missing required core files")
if not all_required:
    issues.append("Missing required Python dependencies")
if not data_exists:
    issues.append("Data directory not found")

if not issues:
    print("✅ ALL CHECKS PASSED! Ready for deployment!")
    print("\n🎯 NEXT STEPS:")
    print("   1. Read DEPLOYMENT_CHECKLIST.md for deployment options")
    print("   2. For HuggingFace: Follow HUGGINGFACE_SETUP.md")
    print("   3. For GitHub: Push to your repository")
    print("   4. Test locally: python app.py")
    sys.exit(0)
else:
    print("❌ VALIDATION FAILED! Issues found:")
    for issue in issues:
        print(f"   - {issue}")
    print("\n🔧 FIX REQUIRED:")
    print("   1. Install missing dependencies: pip install -r requirements.txt")
    print("   2. Ensure all core files are present")
    print("   3. Create data/ directory if missing")
    sys.exit(1)
