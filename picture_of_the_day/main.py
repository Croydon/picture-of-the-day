import argparse
import logging

from picture_of_the_day.api import run_server


logger = logging.getLogger("picture-of-the-day")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def main():
    parser = argparse.ArgumentParser(description="Picture of the Day.")
    subparsers = parser.add_subparsers(dest="command")
    run_parser = subparsers.add_parser("run", help="Run the server that serves the REST API.")
    run_parser.add_argument("--port", type=int, default=8948, help="Port to run the local server on.")

    args = parser.parse_args()

    if args.command == "run":
        run_server(args)
