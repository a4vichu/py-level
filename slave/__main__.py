#!/usr/bin/env python3
import os
import sys
from slave.cli import cli

def main():
    """Main entry point for the slave server CLI"""
    try:
        # Add the project root to Python path
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, project_root)
        
        # Run the CLI
        cli()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 