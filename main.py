#!/usr/bin/env python3
"""
XCUI Test Case Generator - Main Entry Point
"""

import argparse
import sys
from pathlib import Path
from src.agent.xcui_agent import XCUITestAgent


def main():
    parser = argparse.ArgumentParser(
        description="Generate XCUI test cases for SwiftUI projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate tests for entire project
  python main.py --project ./MyApp --output ./MyAppUITests
  
  # Generate tests for specific views
  python main.py --project ./MyApp --output ./MyAppUITests --views LoginView ProfileView
  
  # Generate project summary
  python main.py --project ./MyApp --summary
  
  # Generate test report
  python main.py --project ./MyApp --report
        """
    )
    
    parser.add_argument(
        '--project',
        '-p',
        required=True,
        help='Path to the SwiftUI project directory'
    )
    
    parser.add_argument(
        '--output',
        '-o',
        help='Path where test files will be generated (default: ./UITests)'
    )
    
    parser.add_argument(
        '--config',
        '-c',
        help='Path to configuration file (default: config/agent_config.yaml)'
    )
    
    parser.add_argument(
        '--views',
        '-v',
        nargs='+',
        help='Specific view names to generate tests for'
    )
    
    parser.add_argument(
        '--summary',
        '-s',
        action='store_true',
        help='Display project summary without generating tests'
    )
    
    parser.add_argument(
        '--report',
        '-r',
        action='store_true',
        help='Generate a test generation report'
    )
    
    args = parser.parse_args()
    
    # Validate project path
    project_path = Path(args.project)
    if not project_path.exists():
        print(f"❌ Error: Project path does not exist: {args.project}")
        sys.exit(1)
    
    # Set default output path
    output_path = args.output or './UITests'
    
    # Initialize agent
    print("🚀 Initializing XCUI Test Agent...")
    try:
        agent = XCUITestAgent(
            project_path=args.project,
            output_path=output_path,
            config_path=args.config
        )
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        sys.exit(1)
    
    # Handle different modes
    if args.summary:
        print("\n📊 Project Summary")
        print("=" * 50)
        summary = agent.get_project_summary()
        print(f"Total Views: {summary['total_views']}")
        print(f"Total Components: {summary['total_components']}")
        print(f"Testable Components: {summary['testable_components']}")
        print("\nComponent Breakdown:")
        for comp_type, count in sorted(summary['component_breakdown'].items()):
            print(f"  - {comp_type}: {count}")
        print("\nViews:")
        for view in summary['views']:
            print(f"  - {view}")
        return
    
    if args.report:
        print(agent.generate_test_report())
        return
    
    # Generate tests
    try:
        generated_files = agent.generate_tests(views=args.views)
        
        if generated_files:
            print("\n✅ Successfully generated test files:")
            for view_name, file_path in generated_files.items():
                print(f"   - {view_name}: {file_path}")
        else:
            print("\n⚠️  No test files were generated")
            
    except Exception as e:
        print(f"\n❌ Error generating tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob
