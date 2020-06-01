'Utility for calculating entropy of (un)normalised probability distributions.'
from argparse import (
    ArgumentParser, ArgumentTypeError, ArgumentDefaultsHelpFormatter
)
from collections import defaultdict
from functools import partial
from tabulate import tabulate
import fileinput
import math
import sys


def get_lines_for_inputs(files):
    lines_dict = defaultdict(list)
    for line in fileinput.input(files):
        filename = fileinput.filename()
        line = line.strip()
        if line == '':
            continue
        lines_dict[filename].append(line)

    for filename, lines in lines_dict.items():
        yield filename, lines


def lines_to_float(lines):
    for line in lines:
        try:
            yield float(line)
        except ValueError:
            raise ValueError(f"Couldn't convert line to float! ({line})")


def all_positive_or_zero(numbers):
    return all(number >= 0 for number in numbers)


def normalise(numbers, check_normalised=False):
    numbers = list(numbers)
    if not all_positive_or_zero(numbers):
        raise ValueError("Number are not all positive or zero!")
    total = sum(numbers)

    if check_normalised and not math.isclose(total, 1.0):
        raise ValueError(f"Entries are not normalised!")

    for number in numbers:
        try:
            yield number / total
        except ZeroDivisionError:
            raise ZeroDivisionError("Couldn't normalise, numbers summed to 1!")


def get_entropy(p_vector, base=math.e):
    information_values = [
        0 if entry == 0 else -entry * math.log(entry, base)
        for entry in p_vector
    ]

    return sum(information_values)


def process_entry(filename, lines, args):
    try:
        weights = lines_to_float(lines)
        probability_vector = list(normalise(weights, args.check_normalised))
    except ValueError as e:
        print(f"Error occured processing {filename}: {e}", file=sys.stderr)
        return

    entropy = get_entropy(probability_vector, base=args.base)

    return entropy


def remove_invalid(entries):
    for entry in entries:
        if all(value is not None for value in entry):
            yield entry


def positive_int(value):
    as_int = int(value)
    if as_int < 0:
        raise ArgumentTypeError(
            "Precision must be a positive (or zero) integer!"
            f" Got {as_int}."
        )

    return as_int


def build_parser():
    parser = ArgumentParser(
        description=__doc__,
        formatter_class=ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        'files',
        nargs='*',
        metavar='FILES',
        help=(
            "Files to read. One value per line. "
            "Blank lines ignored. - is stdin. "
            "If no files given read from stdin."
        )
    )

    parser.add_argument(
        '--no-filenames',
        action='store_true',
        help="Don't print filenames."
    )

    parser.add_argument(
        '-c', '--check-normalised',
        action='store_true',
        help="Don't print filenames."
    )

    parser.add_argument(
        '--precision', type=positive_int, default=3,
        metavar='PREC',
        help="Precision for printing."
    )

    parser.add_argument(
        '--base', type=float, default=math.e,
        help='Base for logarithm.'
    )

    return parser


def main():
    args = build_parser().parse_args()

    output_table = [
        (filename, process_entry(filename, lines, args))
        for filename, lines in get_lines_for_inputs(args.files)
    ]
    output_table = list(remove_invalid(output_table))
    if len(output_table) == 0:
        return

    if args.no_filenames:
        output_table = [(entropy, ) for (fn, entropy) in output_table]

    float_format = f".{args.precision}f"
    print(tabulate(output_table, tablefmt='plain', floatfmt=float_format))


if __name__ == '__main__':
    main()
