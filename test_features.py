
"""
Test script to verify all Aetherium features are working
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from brain import AetheriumBrain
from commands import (
    handle_system_command,
    handle_process_list,
    handle_disk_usage,
    handle_network_info,
    handle_system_uptime,
    handle_users_logged_in,
    handle_environment_variables,
    handle_running_services,
    list_files,
    create_file,
    read_file,
    delete_file,
    execute_command
)

def test_all_features():
    print("🧪 Testing Aetherium Features...\n")
    
    brain = AetheriumBrain()
    test_results = {}
    
    # Test all available commands
    test_commands = [
        ("list files", list_files),
        ("system info", handle_system_command),
        ("create test_file.txt", lambda: create_file("test_file.txt", "Test content")),
        ("read test_file.txt", lambda: read_file("test_file.txt")),
        ("disk usage", handle_disk_usage),
        ("running processes", handle_process_list),
        ("network info", handle_network_info),
        ("uptime", handle_system_uptime),
        ("users online", handle_users_logged_in),
        ("environment variables", handle_environment_variables),
        ("running services", handle_running_services),
        ("run dir", lambda: execute_command("dir" if os.name == 'nt' else "ls"))
    ]
    
    for command_name, command_func in test_commands:
        try:
            print(f"Testing: {command_name}")
            result = command_func()
            if "error" in result.lower() or "not found" in result.lower():
                test_results[command_name] = "❌ FAILED"
                print(f"   Result: ❌ FAILED - {result}")
            else:
                test_results[command_name] = "✅ PASSED"
                print(f"   Result: ✅ PASSED")
        except Exception as e:
            test_results[command_name] = f"❌ ERROR: {e}"
            print(f"   Result: ❌ ERROR - {e}")
        print()
    
    # Test AI intent recognition for all features
    print("🤖 Testing AI Intent Recognition...\n")
    test_phrases = [
        "hello there",
        "list my files",
        "show system information",
        "create a new file",
        "what's running on my system",
        "check disk space",
        "show network info",
        "system uptime",
        "who is logged in",
        "show environment variables",
        "running services",
        "run command"
    ]
    
    for phrase in test_phrases:
        intent = brain.predict_intent(phrase)
        print(f"'{phrase}' -> {intent['tag']}: {intent['response']}")
    
    # Test file operations
    print("\n📁 Testing File Operations...")
    try:
        # Create test file
        create_result = create_file("test_feature.txt", "Testing Aetherium features")
        print(f"Create: {create_result}")
        
        # Read test file
        read_result = read_file("test_feature.txt")
        print(f"Read: {read_result[:100]}...")
        
        # Delete test file
        delete_result = delete_file("test_feature.txt")
        print(f"Delete: {delete_result}")
        
        test_results["file_operations"] = "✅ PASSED"
    except Exception as e:
        test_results["file_operations"] = f"❌ ERROR: {e}"
        print(f"File operations failed: {e}")
    
    # Cleanup
    if os.path.exists("test_file.txt"):
        delete_file("test_file.txt")
    if os.path.exists("test_feature.txt"):
        delete_file("test_feature.txt")
    
    # Print summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    for test, result in test_results.items():
        print(f"{test:25} : {result}")
    
    passed = sum(1 for r in test_results.values() if "PASSED" in r)
    total = len(test_results)
    
    print(f"\n✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Aetherium is working perfectly!")
        print("\n🚀 You can now:")
        print("  • Run CLI: python main.py help")
        print("  • Run GUI: python main.py gui")
        print("  • Chat mode: python main.py chat")
        print("  • Test features: python test_features.py")
    else:
        print("⚠️  Some tests failed. Check the implementation.")
    
    return passed == total

def test_cli_commands():
    """Test CLI command functionality"""
    print("\n🖥️ Testing CLI Commands...")
    
    # Test that all CLI functions can be imported and called
    try:
        from main import process_command
        
        test_inputs = [
            "hello",
            "list files",
            "system info",
            "create test.txt",
            "disk usage",
            "uptime"
        ]
        
        for test_input in test_inputs:
            try:
                result = process_command(test_input)
                print(f"✅ '{test_input}' -> {result[:50]}...")
            except Exception as e:
                print(f"❌ '{test_input}' failed: {e}")
                
    except ImportError as e:
        print(f"❌ Could not import CLI functions: {e}")

if __name__ == "__main__":
    success = test_all_features()
    test_cli_commands()
    
    if success:
        print("\n🎯 Aetherium is ready for use!")
    else:
        print("\n🔧 Please fix the failing tests before using Aetherium.")