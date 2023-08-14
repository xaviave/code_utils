import argparse


class DictAction(argparse.Action):
    """
    Action to create a dict of the values in it instead of a tuple of the values

    Examples
    --------

    parser = argparse.ArgumentParser(
            prog=prog, conflict_handler="resolve", add_help=False
        )
    parser.add_argument(
        "-c",
        "--credentials",
        nargs=2,
        type=str,
        dest="credentials",
        action=DictAction,
        custom_name="basic_auth",
        help="Get credential from the arguments"
    )

    >>  '-c username password' option will generate:
            credentials={"basic_auth": (username, password)}
    """

    def __init__(self, option_strings, custom_name, *args, **kwargs):
        self.custom_name = custom_name
        super().__init__(option_strings=option_strings, *args, **kwargs)

    def __call__(self, parser, args, values, option_string=None):
        # will raise an ValueError if failing
        values = {self.custom_name: (values[0], values[1])}
        setattr(args, self.dest, values)
