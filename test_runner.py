# Comprehensive test suite that runs all pathfinding algorithms on all map configurations
import subprocess
import sys
import os
from pathlib import Path

def run_algorithm_test(map_file, algorithm, debug=False):
    cmd = [sys.executable, 'main.py', '--map', map_file, '--algo', algorithm]
    if debug:
        cmd.append('--debug')
    
    print(f"Running {algorithm.upper()} on {map_file}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ SUCCESS")
        print(result.stdout)
    else:
        print("❌ FAILED")
        print(result.stderr)
    
    return result.returncode == 0

def main():
    maps_dir = Path('maps')
    algorithms = ['bfs', 'ucs', 'a_star', 'dynamic_demo']
    
    print("🧪 Running comprehensive test suite...")
    print("=" * 50)
    
    total_tests = 0
    passed_tests = 0
    
    for map_file in maps_dir.glob('*.txt'):
        for algo in algorithms:
            total_tests += 1
            if run_algorithm_test(str(map_file), algo):
                passed_tests += 1
            print("-" * 30)
    
    print(f"\n📊 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
