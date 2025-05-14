"""This module contains the parser for CLI params."""

import argparse


def build_parser():
    """Builds parser for CLI params.

    Returns
    -------
    parser : argparse.ArgumentParser
        The parser object.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-c",
                        "--config",
                        type=str,
                        default="config.ini",
                        help="Path to the configuration file. The default is "
                        "config.ini.")

    return parser
