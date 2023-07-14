import argparse
import json
import logging
import os
import subprocess
from typing import Optional

import toml


class Configuration:
    """Handle configuration related operations."""

    def __init__(self, config_file_path: str):
        if not os.path.isfile(config_file_path):
            raise FileNotFoundError(f"The configuration file does not exist: {config_file_path}")
        if not os.access(config_file_path, os.R_OK):
            raise PermissionError(f"The configuration file is not readable: {config_file_path}")
        self.config_file_path = config_file_path
        self.data = self.load()

    def load(self):
        """Load configuration from the given file path."""
        try:
            return toml.load(self.config_file_path)
        except Exception as e:
            logging.error(f"Failed to load configuration file: {self.config_file_path}")
            raise RuntimeError("Could not load the configuration file.") from e

    @property
    def stack_name(self) -> Optional[str]:
        """Retrieve stack name from the configuration."""
        stack_name = (
            self.data.get("default", {}).get("deploy", {}).get("parameters", {}).get("stack_name")
        )
        if not stack_name:
            raise ValueError("Stack name not found in the configuration.")
        return stack_name


class AWSStack:
    """Handle AWS Stack operations."""

    def __init__(self, stack_name: str):
        if not stack_name:
            raise ValueError("Stack name must not be empty.")
        self.stack_name = stack_name

    def fetch_output(self) -> list:
        """Fetch the stack output by invoking the AWS CLI."""
        try:
            output = subprocess.check_output(
                [
                    "aws",
                    "cloudformation",
                    "describe-stacks",
                    "--stack-name",
                    self.stack_name,
                    "--query",
                    "Stacks[0].Outputs",
                    "--output",
                    "json",
                ],
                stderr=subprocess.STDOUT,
            )
            return json.loads(output)
        except Exception as e:
            logging.error("Failed to fetch stack outputs.")
            raise RuntimeError("Could not fetch the stack outputs.") from e

    def find_output_value(self, output_key: str) -> Optional[str]:
        """Find the value of the given output key in the stack output."""
        output = self.fetch_output()
        return next(
            (item["OutputValue"] for item in output if item["OutputKey"] == output_key),
            None,
        )


def parse_arguments():
    """Parse and validate command line arguments."""
    parser = argparse.ArgumentParser(
        description="Extract a specific variable from AWS Stack Information."
    )
    parser.add_argument(
        "output_key",
        help="The output key to extract from the stack information.",
    )
    parser.add_argument(
        "var_name",
        help="The variable name to be saved in GitHub",
    )
    args = parser.parse_args()

    if not args.output_key or not isinstance(args.output_key, str):
        raise argparse.ArgumentTypeError("Output key is required and must be a string.")
    if not args.var_name or not isinstance(args.var_name, str):
        raise argparse.ArgumentTypeError("Variable name is required and must be a string.")

    return args


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    args = parse_arguments()

    try:
        config = Configuration(os.getenv("CONFIG_FILE_PATH"))
        stack = AWSStack(config.stack_name)
        output_value = stack.find_output_value(args.output_key)

        if output_value is None:
            logging.warning(f"Output key '{args.output_key}' not found in the stack " "outputs.")
        else:
            with open(os.getenv("GITHUB_ENV"), "a") as file:
                file.write(f"{args.var_name}={output_value}\n")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    main()
