"""
Command-line interface for the Intelligent Code Reviewer.
"""

import sys
import os
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from reviewer import CodeReviewer
from models import Language


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="🤖 Intelligent Code Reviewer & Explainer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Review a Python file
  python main.py samples/sample_bad.py
  
  # Review with explicit language
  python main.py --lang javascript script.js
  
  # Review code directly
  python main.py --code "print('hello')" --lang python
        """
    )
    
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to code file to review"
    )
    
    parser.add_argument(
        "-c", "--code",
        help="Code string to review (alternative to file)"
    )
    
    parser.add_argument(
        "-l", "--lang",
        choices=[lang.value for lang in Language],
        help="Programming language (if not detected from file)"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file for results (JSON format)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Check input
    if not args.file and not args.code:
        print("❌ Please provide either a file path or code string")
        print("Use --help for usage information")
        sys.exit(1)
    
    # Initialize reviewer
    try:
        reviewer = CodeReviewer(provider="groq")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        sys.exit(1)
    
    # Review code
    try:
        if args.file:
            results = reviewer.review_file(args.file)
        else:
            language = args.lang or "python"
            results = reviewer.review_code(
                code=args.code,
                language=language
            )
        
        # Render results
        reviewer.render_results(results)
        
        # Save output if requested
        if args.output:
            import json
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"💾 Results saved to: {args.output}")
        
        # Verbose output
        if args.verbose:
            print("\n📊 Metadata:")
            for key, value in results.get('metadata', {}).items():
                print(f"   {key}: {value}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()