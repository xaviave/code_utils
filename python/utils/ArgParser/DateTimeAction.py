import argparse
import datetime


class DateTimeAction(argparse.Action):
    """
    Use of a custom action to validate the format of datetime in values

    Examples
    --------

    parser = argparse.ArgumentParser(
            prog=prog, conflict_handler="resolve", add_help=False
    )
    parser.add_argument(
        "-t",
        "--timerange",
        nargs=2,
        type=str,
        action=DateTimeAction,
        default=(datetime.datetime.now() - datetime.timedelta(days=1), datetime.datetime.now()),
        help="Get the query's timerange | 2 strings with format: 'YYYY-MM-DDTHH:MM:SS'"
    )
    """

    def __call__(self, parser, args, values, option_string=None):
        _format = "%Y-%m-%d %H:%M:%S"
        try:
            values = (datetime.datetime.strptime(v, _format) for v in values)
        except ValueError:
            raise ValueError(
                "\n\tThe datetime string is not well formated\n\tUse this template: '%Y-%m-%d %H:%M:%S'"
            )
        setattr(args, self.dest, values)
