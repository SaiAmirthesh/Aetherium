
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
    
    # Test commands
    test_commands = [
        ("list files", list_files),
        ("system info", handle_system_command),
        ("create test_file.txt", lambda: create_file("test_file.txt", "Test content")),
        ("read test_file.txt", lambda: read_file("test_file.txt")),
        ("disk usage", handle_disk_usage),
        ("running processes", handle_process_list),
        ("network info", handle_network_info),
        ("uptime", handle_system_uptime),
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
    
    # Test AI intent recognition
    print("🤖 Testing AI Intent Recognition...\n")
    test_phrases = [
        "hello there",
        "list my files",
        "show system information",
        "create a new file",
        "what's running on my system",
        "check disk space"
    ]
    
    for phrase in test_phrases:
        intent = brain.predict_intent(phrase)
        print(f"'{phrase}' -> {intent['tag']}: {intent['response']}")
    
    # Cleanup
    if os.path.exists("test_file.txt"):
        delete_file("test_file.txt")
    
    # Print summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    for test, result in test_results.items():
        print(f"{test:20} : {result}")
    
    passed = sum(1 for r in test_results.values() if "PASSED" in r)
    total = len(test_results)
    
    print(f"\n✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Aetherium is working perfectly!")
    else:
        print("⚠️  Some tests failed. Check the implementation.")

if __name__ == "__main__":
    test_all_features()