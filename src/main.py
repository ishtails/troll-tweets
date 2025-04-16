"""Main entry point for the application."""

import argparse
from .eda import eda

def main():
    """Main entry point for the application."""

    parser = argparse.ArgumentParser(description="Main CLI for troll tweets project.")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # EDA subcommand
    eda_parser = subparsers.add_parser("eda", help="Run exploratory data analysis")
    eda_parser.set_defaults(func=eda)

    args = parser.parse_args()
    if args.command:
        args.func()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
