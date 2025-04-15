"""Main entry point for the application."""

from .preprocessing.processor import process_tweets


def main():
    """Main entry point for the application."""
    process_tweets()


if __name__ == "__main__":
    main()
