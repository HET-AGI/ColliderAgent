#!/usr/bin/env python3
"""
Test script for MadGraph5 tool.

Tests the connect_to_madgraph() function.

Usage:
    python test_madgraph_tools.py
    python test_madgraph_tools.py --full  # Run full event generation test
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from tools.madgraph_tools import connect_to_madgraph


def test_simple_commands():
    """Test simple MadGraph5 commands."""
    print("\n" + "="*60)
    print("TEST 1: Simple Commands (import model, display)")
    print("="*60)

    script = """
import model sm
display particles
exit
"""
    result = connect_to_madgraph(script, timeout=60)

    print(f"Success: {result['success']}")
    print(f"Return Code: {result['return_code']}")
    print(f"Message: {result['message']}")

    if result['stdout']:
        print("\nStdout (first 500 chars):")
        print("-"*40)
        print(result['stdout'][:500])
        print("-"*40)

    return result['success']


def test_generate_process():
    """Test process generation (no launch)."""
    print("\n" + "="*60)
    print("TEST 2: Generate Process (No Launch)")
    print("="*60)

    script = """
import model sm
generate p p > mu+ mu-
output outputs/test_pp_mumu_simple
"""
    result = connect_to_madgraph(script, timeout=120)

    print(f"Success: {result['success']}")
    print(f"Return Code: {result['return_code']}")
    print(f"Message: {result['message']}")

    # Check if output directory was created
    output_dir = Path("outputs/test_pp_mumu_simple")
    if output_dir.exists():
        print(f"\nOutput directory created: {output_dir}")
        print("Contents:")
        for item in sorted(output_dir.iterdir())[:10]:
            print(f"  - {item.name}")
    else:
        print(f"\nOutput directory not found: {output_dir}")

    return result['success']


def test_full_generation():
    """Test full event generation."""
    print("\n" + "="*60)
    print("TEST 3: Full Event Generation")
    print("="*60)

    script = """
import model sm
generate p p > e+ e-
output outputs/test_full_pp_ee
launch outputs/test_full_pp_ee
set nevents 100
set ebeam1 6500
set ebeam2 6500
0
"""
    result = connect_to_madgraph(script, timeout=600)

    print(f"Success: {result['success']}")
    print(f"Return Code: {result['return_code']}")
    print(f"Message: {result['message']}")

    # Check for events file
    import glob
    events_pattern = "outputs/test_full_pp_ee/Events/run_*/unweighted_events.lhe.gz"
    events_files = glob.glob(events_pattern)

    if events_files:
        print(f"\nEvents file generated: {events_files[-1]}")
    else:
        print("\nNo events file found")

    return result['success']


def main():
    """Run all tests."""
    import argparse

    parser = argparse.ArgumentParser(description="Test MadGraph5 tool")
    parser.add_argument("--full", action="store_true", help="Run full event generation test")
    args = parser.parse_args()

    print("\n" + "="*60)
    print("MadGraph5 Tool Test Suite")
    print("="*60)

    # Check MG5_PATH
    mg5_path = os.getenv("MG5_PATH")
    print(f"\nMG5_PATH: {mg5_path}")

    if not mg5_path:
        print("\nERROR: MG5_PATH environment variable not set!")
        print("Please set MG5_PATH in .env file or environment.")
        sys.exit(1)

    results = {}

    # Test 1: Simple commands
    results['simple_commands'] = test_simple_commands()

    # Test 2: Process generation
    results['generate_process'] = test_generate_process()

    # Test 3: Full generation (optional)
    if args.full:
        results['full_generation'] = test_full_generation()

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    for test_name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"  {test_name}: {status}")

    all_passed = all(results.values())
    print("\n" + ("All tests passed!" if all_passed else "Some tests failed."))

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
