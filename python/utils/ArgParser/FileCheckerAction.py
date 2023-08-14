import os
import argparse
from functools import cached_property

import puremagic


class FileCheckerAction(argparse.Action):
    """
    Action class used in Argparse to validate and parse data from files
    during the Argparse process


    Examples
    --------

    parser = argparse.ArgumentParser(
            prog=prog, conflict_handler="resolve", add_help=False
        )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        action=FileCheckerAction,
        default=os.path.join("folder", "file.txt"),
        help=f"Provide file path",
        dest="path_file"
    )
    """

    def _argument_validator(self, values) -> list:
        # Add your validations and checks
        raise NotImplementedError

    @cached_property
    def _allowed_extensions(self) -> list:
        # return [".txt", ".pdf"]
        raise NotImplementedError

    def _check_media_type(self, path: str) -> None:
        """
        check file path and file type
        """
        if not path or not os.path.exists(path):
            raise FileNotFoundError("File Path doesnt exist")
        # get magic number to get the file type else use file extension
        ftype: str = puremagic.from_file(path)
        if ftype not in self._allowed_extensions:
            raise AttributeError(f"File extension: {ftype} is not valid '{path}'")

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if not os.path.exists(values) or self._check_media_type(values):
            raise ValueError(f"File '{values}' does not exist or is in the wrong format (TXT)")
        self._argument_validator(values)
        setattr(namespace, self.dest, values)
