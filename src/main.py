#!/usr/bin/env python3
"""
Main entry point for the log-analyzer CLI.
"""
import argparse
import sys
import json
from __init__ import __version__
from parser import count_levels
def main():
    parser = argparse.ArgumentParser(
        description="CLI log analyzer that parses log files or stdin, "
                    "counts errors/warnings by level, and outputs summaries."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "logfile",
        nargs="?",
        default=None,
        help="Path to log file (default: read from stdin)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="Output format: 'text' or 'json' (default: text)"
    )
    args = parser.parse_args()
    # Read input
    if args.logfile:
        try:
            with open(args.logfile, "r", encoding="utf-8") as f:
                counts = count_levels(f)
        except FileNotFoundError:
            print(f"Error: Log file '{args.logfile}' not found.", file=sys.stderr)
            sys.exit(2)
        except Exception as e:
            print(f"Error reading '{args.logfile}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        counts = count_levels(sys.stdin)
    # Output
    if args.format == "json":
        print(json.dumps(dict(counts), indent=2, sort_keys=True))
    else:
        if counts:
            for level in sorted(counts):
                print(f"{level}: {counts[level]}")
        else:
            print("No recognized log levels found.")
if __name__ == "__main__":
    main()