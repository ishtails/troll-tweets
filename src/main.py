"""Main entry point for the application."""

import argparse
from .preprocessing import process_tweets
from .EDA import run_eda

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Main CLI for troll tweets project.")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Preprocess subcommand
    preprocess_parser = subparsers.add_parser(
        "preprocess", help="Run tweet preprocessing"
    )
    preprocess_parser.set_defaults(func=process_tweets)

    # EDA subcommand
    eda_parser = subparsers.add_parser("eda", help="Run exploratory data analysis")
    eda_parser.set_defaults(func=run_eda)

    args = parser.parse_args()
    if args.command:
        args.func()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
