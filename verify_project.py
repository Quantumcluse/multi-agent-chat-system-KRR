"""
Project Verification Script
Checks that all required components are in place
"""
import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    return exists

def check_directory_exists(dirpath, description):
    """Check if directory exists"""
    exists = os.path.isdir(dirpath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {dirpath}")
    return exists

def main():
    """Main verification function"""
    print("=" * 80)
    print("PROJECT VERIFICATION")
    print("=" * 80)
    print()
    
    all_checks = []
    
    print("Core Components:")
    all_checks.append(check_file_exists("core/config.py", "Config module"))
    all_checks.append(check_file_exists("core/message.py", "Message protocol"))
    all_checks.append(check_file_exists("core/logger.py", "Logging system"))
    print()
    
    print("Agent Implementations:")
    all_checks.append(check_file_exists("agents/coordinator.py", "Coordinator agent"))
    all_checks.append(check_file_exists("agents/research_agent.py", "Research agent"))
    all_checks.append(check_file_exists("agents/analysis_agent.py", "Analysis agent"))
    all_checks.append(check_file_exists("agents/memory_agent.py", "Memory agent"))
    print()
    
    print("Memory System:")
    all_checks.append(check_file_exists("memory/knowledge_base.py", "Knowledge base"))
    all_checks.append(check_file_exists("memory/vector_store.py", "Vector store"))
    print()
    
    print("Entry Points:")
    all_checks.append(check_file_exists("main.py", "Interactive main"))
    all_checks.append(check_file_exists("run_scenarios.py", "Test scenarios"))
    print()
    
    print("Docker Configuration:")
    all_checks.append(check_file_exists("Dockerfile", "Dockerfile"))
    all_checks.append(check_file_exists("docker-compose.yml", "Docker Compose"))
    print()
    
    print("Documentation:")
    all_checks.append(check_file_exists("README.md", "README"))
    all_checks.append(check_file_exists("requirements.txt", "Requirements"))
    print()
    
    print("Test Outputs:")
    all_checks.append(check_directory_exists("outputs", "Outputs directory"))
    all_checks.append(check_file_exists("outputs/simple_query.txt", "Simple query output"))
    all_checks.append(check_file_exists("outputs/complex_query.txt", "Complex query output"))
    all_checks.append(check_file_exists("outputs/memory_test.txt", "Memory test output"))
    all_checks.append(check_file_exists("outputs/multi_step.txt", "Multi-step output"))
    all_checks.append(check_file_exists("outputs/collaborative.txt", "Collaborative output"))
    print()
    
    # Summary
    passed = sum(all_checks)
    total = len(all_checks)
    
    print("=" * 80)
    print(f"VERIFICATION SUMMARY: {passed}/{total} checks passed")
    print("=" * 80)
    
    if passed == total:
        print("✅ ALL CHECKS PASSED - PROJECT IS COMPLETE")
        return 0
    else:
        print("❌ SOME CHECKS FAILED - REVIEW ABOVE")
        return 1

if __name__ == "__main__":
    sys.exit(main())
